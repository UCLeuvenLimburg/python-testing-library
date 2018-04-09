from ucll_scripting.formatting import *
import unittest


class FormattingTests(unittest.TestCase):
    def test_hbox_empty(self):
        lines = hbox().format()
        assert len(lines) == 0

    def test_hbox_single_line(self):
        lines = hbox('a', 'b', 'c').format()

        assert len(lines) == 1
        assert lines[0] == 'abc'

    def test_hbox_single_column(self):
        col1 = vbox('a', 'bb', 'ccc')
        lines = hbox(col1).format()

        assert len(lines) == 3
        assert lines[0] == 'a  '
        assert lines[1] == 'bb '
        assert lines[2] == 'ccc'

    def test_hbox_single_column_right_align(self):
        col1 = vbox('a', 'bb', 'ccc')
        lines = hbox(col1, halign=HorizontalAlignment.right).format()

        assert len(lines) == 3
        assert lines[0] == '  a'
        assert lines[1] == ' bb'
        assert lines[2] == 'ccc'

    def test_hbox_single_column_centered(self):
        col1 = vbox('a', 'bb', 'ccc')
        lines = hbox(col1, halign=HorizontalAlignment.center).format()

        assert len(lines) == 3
        assert lines[0] == ' a '
        assert lines[1] == ' bb'
        assert lines[2] == 'ccc'
        
    def test_hbox_of_vboxes(self):
        col1 = vbox('a')
        col2 = vbox('a', 'b')
        col3 = vbox('a', 'bb')
        lines = hbox(col1, col2, col3).format()

        assert len(lines) == 2
        assert lines[0] == 'aaa '
        assert lines[1] == ' bbb'
        
    def test_vbox_abc(self):
        lines = vbox('a', 'b', 'c').format()

        assert len(lines) == 3
        assert lines[0] == 'a'
        assert lines[1] == 'b'
        assert lines[2] == 'c'

    def test_indentation_single_line(self):
        lines = indent(4, 'abc').format()

        assert len(lines) == 1
        assert lines[0] == '    abc'

    def test_indentation_multiple_lines(self):
        lines = indent(4, vbox('a', 'b', 'c')).format()

        assert len(lines) == 3
        assert lines[0] == '    a'
        assert lines[1] == '    b'
        assert lines[2] == '    c'
