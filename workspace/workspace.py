from lxml import etree
from xml.etree import ElementTree as ET

from xblock.core import XBlock
from xblock.fields import Scope, List, String
from xblock.fragment import Fragment

from .utils import load_resource, render_template

from StringIO import StringIO


class WorkspaceBlock(XBlock):
    """
    An XBlock providing a responsive multimedia carousel and workspace
    """

    display_name = String(help="This name appears in horizontal navigation at the top of the page.",
                          default="Workspace",
                          scope=Scope.content
    )

    data = List(help="This is the representation of the data items as a list of tuples ",
                default=[('img', 'http://met-content.bu.edu/etr2/content/images/Slide5.JPG', '100%', '96'),
                         ('img', 'http://met-content.bu.edu/etr2/content/images/Slide6.JPG', '100%', '96'),
                         ('img', 'http://met-content.bu.edu/etr2/content/images/Slide7.JPG', '100%', '96')],
                scope=Scope.content
    )

    href = String(help="workspace url",
                          default=None,
                          scope=Scope.content
    )

    def student_view(self, context):
        """
        Lab view, displayed to the student
        """
        fragment = Fragment()

        context = {
            'items': self.data,
            'url': self.href
        }

        fragment.add_content(render_template('/templates/html/workspace.html', context))
        fragment.add_javascript(load_resource('public/js/jquery-ui-1.10.4.custom.js'))
        fragment.add_css(load_resource('public/css/responsive-carousel.css'))
        fragment.add_css(load_resource('public/css/responsive-carousel.slide.css'))
        fragment.add_javascript(load_resource('public/js/responsive-carousel.js'))
        fragment.add_css(load_resource("public/css/video-js.css"))
        fragment.add_javascript(load_resource("public/js/video.js"))
        fragment.add_javascript(load_resource('public/js/youtube.js'))
        fragment.add_javascript("function WorkspaceBlock(runtime, element) { $('.carousel').carousel(); }")
        fragment.initialize_js("WorkspaceBlock")

        return fragment

    def studio_view(self, context):
        """
        Studio edit view
        """
        xml_data = self._build_xml(self.data)

        fragment = Fragment()
        fragment.add_content(render_template('templates/html/workspace_edit.html', {'xml_data': xml_data, self: self}))
        fragment.add_javascript(load_resource('public/js/jquery-ui-1.10.4.custom.js'))
        fragment.add_javascript(load_resource('public/js/workspace_edit.js'))
        fragment.initialize_js('WorkspaceEditBlock')

        return fragment

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):
        self.display_name = submissions['display_name']
        self.href = submissions['workspace_url']
        xml_content = submissions['data']

        try:
            etree.parse(StringIO(xml_content))
            xmltree = etree.fromstring(xml_content)
            items_list = self._get_items(xmltree)
            self.data = items_list

        except etree.XMLSyntaxError as e:
            return {
                'result': 'error',
                'message': e.message
            }

        return {
            'result': 'success',
        }

    def _get_items(self, xmltree):
        """
        Helper method
        """
        items_elements = xmltree.getchildren()
        items = []
        for item_element in items_elements:
            item_tag = item_element.tag
            item_src = item_element.get('src')
            item_width = item_element.get('width', '100%')
            item_height = item_element.get('height', '625')
            items.append((item_tag, item_src, item_width, item_height))

        return items

    def _build_xml(self, items_list):
        """
        Helper method
        """
        xml = etree.Element('workspace')
        for item in items_list:
            tag = etree.SubElement(xml, item[0], src=item[1], width=item[2], height=item[3])
        return etree.tostring(xml, pretty_print=True)

    @staticmethod
    def workbench_scenarios():
        return [("workspace demo", "<workspace />")]
