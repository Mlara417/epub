import unittest
from unittest.mock import patch, MagicMock
from cli.src.epub3 import Epub3
import os
import json
from cli.src.exceptions import ValidationError

class TestEpub3(unittest.TestCase):

    @patch('cli.src.epub3.Xml')
    def setUp(self, MockXml):
        self.mock_xml_instance = MockXml.return_value
        self.epub = Epub3(workspace='test_workspace')
        self.epub.xml = self.mock_xml_instance

    def test_init(self):
        self.assertEqual(self.epub.workspace, 'test_workspace')

    @patch('os.mkdir')
    @patch('cli.src.epub3.unzip_file')
    def test_init_creates_workspace(self, mock_unzip, mock_mkdir):
        self.epub.init('test.epub')
        mock_mkdir.assert_called_once_with('test_workspace')
        mock_unzip.assert_called_once_with('test.epub', 'test_workspace')

    @patch('cli.src.epub3.success')
    def test_add_manifest_subnode(self, mock_success):
        self.epub.add_manifest_subnode('item', {'href': 'content.xhtml', 'id': 'item1'})
        mock_success.assert_called_once_with("Adding manifest subnode: item")

    @patch('cli.src.epub3.success')
    def test_add_metadata_subnode(self, mock_success):
        self.epub.add_metadata_subnode('title', {'content': 'Test Title'})
        mock_success.assert_called_once_with("Adding metadata subnode: title")

    @patch('cli.src.epub3.success')
    def test_add_spine_subnode(self, mock_success):
        self.epub.add_spine_subnode('itemref', {'idref': 'item1'})
        mock_success.assert_called_once_with("Adding spine subnode: itemref")

    @patch('os.path.exists')
    @patch('shutil.rmtree')
    def test_cleanup_removes_workspace(self, mock_rmtree, mock_exists):
        mock_exists.return_value = True
        self.epub.cleanup()
        mock_rmtree.assert_called_once_with('test_workspace')

    @patch('os.path.exists')
    def test_cleanup_raises_error_if_workspace_does_not_exist(self, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            self.epub.cleanup()

    @patch('cli.src.epub3.success')
    @patch('cli.src.epub3.zip_file')
    def test_package_epub(self, mock_zip, mock_success):
        self.epub.package_epub('output.epub')
        self.assertEqual(mock_success.call_count, 2)
        mock_success.assert_any_call("Packaging EPUB file...")
        mock_success.assert_any_call("EPUB file packaged: output.epub")
        mock_zip.assert_any_call("-X0", 'output.epub', "mimetype", 'test_workspace')
        mock_zip.assert_any_call("-Xr9D", "..output.epub", ".", 'test_workspace')

    @patch('cli.src.epub3.EpubCheck')
    @patch('cli.src.epub3.error')
    @patch('json.dumps')
    def test_validate_epub_with_issues(self, mock_json_dumps, mock_error, MockEpubCheck):
        # Assume ValidationError now takes a positional argument.
        mock_check = MockEpubCheck.return_value
        mock_check.messages = ["Error 1", "Error 2"]
        with self.assertRaises(ValidationError):
            self.epub.validate_epub('output.epub')
        mock_error.assert_called_once_with("EPUB file has validation issues")
        mock_json_dumps.assert_called_once_with(mock_check.messages, indent=4)

    @patch('cli.src.epub3.success')
    def test_get_opf_manifest(self, mock_success):
        self.mock_xml_instance.get_node.return_value = 'mock_manifest'
        manifest = self.epub.get_opf_manifest()
        self.assertEqual(manifest, 'mock_manifest')
        mock_success.assert_called_once_with("Getting manifest from content.opf")

    @patch('cli.src.epub3.success')
    def test_get_opf_metadata(self, mock_success):
        self.mock_xml_instance.get_node.return_value = 'mock_metadata'
        metadata = self.epub.get_opf_metadata()
        self.assertEqual(metadata, 'mock_metadata')
        mock_success.assert_called_once_with("Getting metadata from content.opf")

    @patch('cli.src.epub3.warning')
    def test_get_opf_metadata_value_not_found(self, mock_warning):
        self.mock_xml_instance.get_node_value.return_value = None
        with self.assertRaises(ValueError):
            self.epub.get_opf_metadata_value('nonexistent')
        mock_warning.assert_called_once_with("Metadata tag 'nonexistent' not found")

    def test_get_opf_metadata_value_found(self):
        self.mock_xml_instance.get_node_value.return_value = 'mock_value'
        value = self.epub.get_opf_metadata_value('title')
        self.assertEqual(value, 'mock_value')

    def test_get_opf_metadata_info(self):
        self.mock_xml_instance.get_node_value.side_effect = ['Title', 'Author', 'en', '12345', 'Contributor']
        metadata_info = self.epub.get_opf_metadata_info()
        expected_metadata = {
            'title': 'Title',
            'creator': 'Author',
            'language': 'en',
            'identifier': '12345',
            'contributor': 'Contributor'
        }
        self.assertEqual(metadata_info, expected_metadata)

    @patch('os.path.exists')
    @patch('lxml.etree.parse')
    @patch('cli.src.epub3.warning')
    def test_get_toc_file_not_exist(self, mock_warning, mock_parse, mock_exists):
        mock_exists.return_value = False
        toc = self.epub.get_toc()
        self.assertEqual(toc, [])
        mock_warning.assert_called_once_with("TOC file 'test_workspace/toc.xhtml' does not exist")

    @patch('os.path.exists')
    @patch('lxml.etree.parse')
    @patch('cli.src.epub3.warning')
    def test_get_toc_parse_error(self, mock_warning, mock_parse, mock_exists):
        mock_exists.return_value = True
        mock_parse.side_effect = Exception("Parse error")
        with self.assertRaises(ValueError):
            self.epub.get_toc()
        # Expect the warning call before the error is raised.
        mock_warning.assert_called_once_with("Failed to retrieve root element from 'test_workspace/toc.xhtml'")

    @patch('os.path.exists')
    @patch('lxml.etree.parse')
    def test_get_toc_success(self, mock_parse, mock_exists):
        mock_exists.return_value = True

        # Create the nav element with nested structure.
        nav_element = MagicMock()
        li_element = MagicMock()
        a_tag = MagicMock()
        a_tag.text = 'Chapter 1'
        a_tag.get.return_value = 'chapter1.xhtml'
        li_element.find.return_value = a_tag
        nav_element.xpath.return_value = [li_element]

        # The root's xpath returns the nav element.
        mock_root = MagicMock()
        mock_root.xpath.return_value = [nav_element]
        mock_parse.return_value.getroot.return_value = mock_root

        toc = self.epub.get_toc()
        expected_toc = [{"label": "Chapter 1", "content": "chapter1.xhtml", "level": 0}]
        self.assertEqual(toc, expected_toc)

if __name__ == '__main__':
    unittest.main()
