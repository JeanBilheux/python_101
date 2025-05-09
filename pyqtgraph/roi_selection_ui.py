from IPython.core.display import HTML
from IPython.display import display
import numpy as np
import random
from collections import OrderedDict
import pyqtgraph as pg
from qtpy.QtWidgets import QMainWindow, QProgressBar, QVBoxLayout, QTableWidgetSelectionRange, QTableWidgetItem
from qtpy import QtGui
from __code import load_ui
from PIL import Image
import os

from NeuNorm.normalization import Normalization


class Interface(QMainWindow):

    roi_width = 0.01
    roi_selected = {} #nice formatting of list_roi for outside access

    list_of_files = None
    live_data = []
    o_norm = None
    roi_column_width = 70
    integrated_image = None
    integrated_image_size = {'width': -1, 'height': -1}

    array2d = None

    list_roi = {} #  'row": {'x0':None, 'y0': None, 'x1': None, 'y1': None}
    default_roi = {'x0': 0, 'y0': 0, 'x1': 50, 'y1': 50, 'id': None}

    def __init__(self, parent=None,
                 list_files=None):

        self.images = []
        for _file in list_files:
            _image = np.array(Image.open(_file))
            self.images.append(_image)

        super(QMainWindow, self).__init__(parent)
        ui_full_path = os.path.join(os.path.dirname(__file__),
                                    os.path.join('ui', 'ui_roi_selection.ui'))
        self.ui = load_ui(ui_full_path, baseinstance=self)

        self.init_statusbar()
        self.setWindowTitle("Background ROI Selection Tool")

        # self.image_item = pg.PlotItem()
        # self.ui.image_view = pg.ImageView(view=self.image_item)
        self.ui.image_view = pg.ImageView()

        # mouse click work
        self.image_item = self.ui.image_view.getImageItem()
        self.scene = self.image_item.scene()
        self.scene.sigMouseClicked.connect(self.mouse_clicked)
        # self.scene.sigMouseMoved.connect(self.mouse_moved)

        self.proxy = pg.SignalProxy(self.scene.sigMouseMoved, rateLimit=60, slot=self.mouse_moved)

        self.vline = pg.InfiniteLine(angle=90, movable=False)
        self.hline = pg.InfiniteLine(angle=0, movable=False)
        self.ui.image_view.addItem(self.vline)
        self.ui.image_view.addItem(self.hline)

        self.ui.image_view.ui.roiBtn.hide()
        self.ui.image_view.ui.menuBtn.hide()

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.ui.image_view)
        self.ui.widget.setLayout(top_layout)
        self.init_widgets()
        self.integrate_images()
        self.display_image()

    def mouse_moved(self, evt):
        # print("in mouse moved")
        pos = evt[0]

        height = self.integrated_image_size['height']
        width = self.integrated_image_size['width']

        if self.image_item.sceneBoundingRect().contains(pos):
            image_pos = self.image_item.mapFromScene(pos)
            x = int(image_pos.x())
            y = int(image_pos.y())
            if (x >= 0) and (x < width) and (y >= 0) and (y < height):
                self.vline.setPos(x)
                self.hline.setPos(y)

        # if self.scene.sceneBoundingRect().contains(pos):
        #     print("yes in bounding rect")



    def mouse_clicked(self, mouseClickEvent):
        image_pos = self.image_item.mapFromScene(mouseClickEvent.scenePos())
        print(f"{image_pos =}")

        # docs used to find about this
        # https://stackoverflow.com/questions/58526980/how-to-connect-mouse-clicked-signal-to-pyqtgraph-plot-widget
        # https://pyqtgraph.readthedocs.io/en/latest/api_reference/graphicsscene/mouseclickevent.html
        # https://groups.google.com/g/pyqtgraph/c/iAROzor1ldE

    def init_widgets(self):
        nbr_columns = self.ui.table_roi.columnCount()
        for _col in range(nbr_columns):
            self.ui.table_roi.setColumnWidth(_col, self.roi_column_width)

    def init_statusbar(self):
        self.eventProgress = QProgressBar(self.ui.statusbar)
        self.eventProgress.setMinimumSize(20, 14)
        self.eventProgress.setMaximumSize(540, 100)
        self.eventProgress.setVisible(False)
        self.ui.statusbar.addPermanentWidget(self.eventProgress)
        # self.parent.eventProgress = QtGui.QProgressBar(self.ui.statusbar)
        # self.parent.eventProgress.setMinimumSize(20, 14)
        # self.parent.eventProgress.setMaximumSize(540, 100)
        # self.parent.eventProgress.setVisible(False)
        # self.ui.statusbar.addPermanentWidget(self.parent.eventProgress)

    def __get_recap(self, data_array):
        if data_array:
            [height, width] = np.shape(data_array[0])
            nbr_sample = len(data_array)
        else:
            nbr_sample = '0'
            [height, width] = ['N/A', 'N/A']

        return [nbr_sample, height, width]

    def __built_html_table_row_3_columns(self, name, nbr, height, width):
        _html = '<tr><td>' + str(name) + '</td><td>' + str(nbr) + '</td><td>' + str(height) + \
        '*' + str(width) + '</td></tr>'
        return _html

    def recap(self):
        """Display nbr of files loaded and size. This can be used to figure why a normalization failed"""
        [nbr_sample, height_sample, width_sample] = self.__get_recap(self.o_norm.data['sample']['data'])
        [nbr_ob, height_ob, width_ob] = self.__get_recap(self.o_norm.data['ob']['data'])
        [nbr_df, height_df, width_df] = self.__get_recap(self.o_norm.data['df']['data'])

        html =  '<table><tr><td width="30%"><strong>Type</strong></td><td><strong>Number</strong></td><td>' + \
                '<strong>Size (height*width)</strong></td></tr>'
        html += self.__built_html_table_row_3_columns('sample', nbr_sample, height_sample, width_sample)
        html += self.__built_html_table_row_3_columns('ob', nbr_ob, height_ob, width_ob)
        html += self.__built_html_table_row_3_columns('df', nbr_df, height_df, width_df)
        html += '</table>'
        display(HTML(html))

    def integrate_images(self):

        self.integrated_image = np.mean(self.images, axis=0)

        [_height, _width] = np.shape(self.integrated_image)
        self.integrated_image_size['height'] = _height
        self.integrated_image_size['width'] = _width

    def _clean_image(self, image):
        _result_inf = np.where(np.isinf(image))
        image[_result_inf] = np.NaN
        return image

    def display_image(self):
        _image = np.transpose(self.integrated_image)
        _image = self._clean_image(_image)
        self.ui.image_view.setImage(_image)

    def remove_row_entry(self, row):
        _roi_id = self.list_roi[row]['id']
        self.ui.image_view.removeItem(_roi_id)
        del self.list_roi[row]

        #rename row
        new_list_roi = {}
        new_row_index = 0
        for _previous_row_index in self.list_roi.keys():
            new_list_roi[new_row_index] = self.list_roi[_previous_row_index]
            new_row_index += 1
        self.list_roi = new_list_roi

    def remove_roi_button_clicked(self):

        self.ui.table_roi.blockSignals(True)

        _selection = self.ui.table_roi.selectedRanges()
        row = _selection[0].topRow()
        old_nbr_row = self.ui.table_roi.rowCount()

        # remove entry from list of roi
        self.remove_row_entry(row)

        # update table of rois
        self.update_table_roi_ui()
        self.ui.table_roi.blockSignals(False)
        self.check_add_remove_button_widgets_status()

        # update selection
        new_nbr_row = self.ui.table_roi.rowCount()
        if new_nbr_row == 0:
            return

        if row == (old_nbr_row-1):
            row = new_nbr_row - 1

        _new_selection = QTableWidgetSelectionRange(row, 0, row, 3)
        self.ui.table_roi.setRangeSelected(_new_selection, True)

    def clear_table(self):
        nbr_row = self.ui.table_roi.rowCount()
        for _row in np.arange(nbr_row):
            self.ui.table_roi.removeRow(0)

    def update_table_roi_ui(self):
        """Using list_roi as reference, repopulate the table_roi_ui"""

        self.ui.table_roi.blockSignals(True)
        list_roi = self.list_roi

        self.clear_table()

        _index_row = 0
        for _roi_key in list_roi.keys():
            _roi = list_roi[_roi_key]

            self.ui.table_roi.insertRow(_index_row)

            self._set_item_value(_index_row, 0, _roi['x0'])
            # _item = QtGui.QTableWidgetItem(str(_roi['x0']))
            # self.ui.table_roi.setItem(_index_row, 0, _item)

            self._set_item_value(_index_row, 1, _roi['y0'])
            # _item = QtGui.QTableWidgetItem(str(_roi['y0']))
            # self.ui.table_roi.setItem(_index_row, 1, _item)

            self._set_item_value(_index_row, 2, _roi['x1'])
            # _item = QtGui.QTableWidgetItem(str(_roi['x1']))
            # self.ui.table_roi.setItem(_index_row, 2, _item)

            self._set_item_value(_index_row, 3, _roi['y1'])
            # _item = QtGui.QTableWidgetItem(str(_roi['y1']))
            # self.ui.table_roi.setItem(_index_row, 3, _item)

            _index_row += 1

        self.ui.table_roi.blockSignals(False)
        #self.ui.table_roi.itemChanged['QTableWidgetItem*'].connect(self.update_table_roi)

    def _set_item_value(self, row=0, column=0, value=-1):
        _item = QTableWidgetItem(str(value))
        self.ui.table_roi.setItem(row, column, _item)

    def check_roi_validity(self, value, x_axis=True):
        """Make sure the ROI selected or defined stays within the image size"""
        min_value = 0

        value = int(value)

        if x_axis:
            max_value = self.integrated_image_size['width']
        else:
            max_value = self.integrated_image_size['height']

        if value < 0:
            return min_value

        if value > max_value:
            return max_value

        return value

    def update_table_roi(self, item):
        """Using the table_roi_ui as reference, will update the list_roi dictionary"""
        self.ui.table_roi.blockSignals(True)

        nbr_row = self.ui.table_roi.rowCount()
        new_list_roi = OrderedDict()
        old_list_roi = self.list_roi
        for _row in np.arange(nbr_row):
            _roi = {}

            # checking that x0, y0, x1 and y1 stay within the range of the image
            _x0 = self.check_roi_validity(self._get_item_value(_row, 0))
            _y0 = self.check_roi_validity(self._get_item_value(_row, 1), x_axis=False)

            _x1 = self.check_roi_validity(self._get_item_value(_row, 2))
            _y1 = self.check_roi_validity(self._get_item_value(_row, 3), x_axis=False)

            # updating table content (in case some of the roi were out of scope
            self._set_item_value(_row, 0, _x0)
            self._set_item_value(_row, 1, _y0)
            self._set_item_value(_row, 2, _x1)
            self._set_item_value(_row, 3, _y1)

            _roi['x0'] = _x0
            _roi['y0'] = _y0
            _roi['x1'] = _x1
            _roi['y1'] = _y1
            _roi['id'] = old_list_roi[_row]['id']

            new_list_roi[_row] = _roi

        self.list_roi = new_list_roi
        self.update_image_view_item()
        self.ui.table_roi.blockSignals(False)

    def update_image_view_item(self):
        self.clear_roi_on_image_view()

        list_roi = self.list_roi
        for _row in list_roi.keys():
            _roi = list_roi[_row]

            _x0 = int(_roi['x0'])
            _y0 = int(_roi['y0'])
            _x1 = int(_roi['x1'])
            _y1 = int(_roi['y1'])

            _width = np.abs(_x1 - _x0)
            _height = np.abs(_y1 - _y0)

            _roi_id = self.init_roi(x0=_x0, y0=_y0,
                                    width=_width, height=_height)
            _roi['id'] = _roi_id

            list_roi[_row] = _roi

        self.list_roi = list_roi

    def _get_item_value(self, row, column):
        _item = self.ui.table_roi.item(row, column)
        if _item:
            return str(_item.text())
        else:
            return ''

    def roi_manually_moved(self):
        list_roi = self.list_roi

        for _row in list_roi.keys():

            _roi = list_roi[_row]

            roi_id = _roi['id']
            region = roi_id.getArraySlice(self.integrated_image, self.ui.image_view.imageItem)

            x0 = region[0][0].start
            x1 = region[0][0].stop
            y0 = region[0][1].start
            y1 = region[0][1].stop

            _roi['x0'] = x0
            _roi['x1'] = x1
            _roi['y0'] = y0
            _roi['y1'] = y1

            list_roi[_row] = _roi

        self.list_roi = list_roi
        self.update_table_roi_ui()

    def clear_roi_on_image_view(self):
        list_roi = self.list_roi

        for _row in list_roi.keys():

            _roi = list_roi[_row]
            roi_id = _roi['id']
            self.ui.image_view.removeItem(roi_id)

    def add_roi_button_clicked(self):
        self.clear_roi_on_image_view()

        self.ui.table_roi.blockSignals(True)
        _selection = self.ui.table_roi.selectedRanges()
        if _selection:
            row = _selection[0].topRow()
        else:
            row = 0

        # init new row with default value
        self.ui.table_roi.insertRow(row)
        _default_roi = self.default_roi

        _item = QTableWidgetItem(str(_default_roi['x0']))
        self.ui.table_roi.setItem(row, 0, _item)

        _item = QTableWidgetItem(str(_default_roi['y0']))
        self.ui.table_roi.setItem(row, 1, _item)

        _item = QTableWidgetItem(str(_default_roi['x1']))
        self.ui.table_roi.setItem(row, 2, _item)

        _item = QTableWidgetItem(str(_default_roi['y1']))
        self.ui.table_roi.setItem(row, 3, _item)

        # save new list_roi dictionary
        nbr_row = self.ui.table_roi.rowCount()
        list_roi = OrderedDict()
        for _row in np.arange(nbr_row):
            _roi = {}

            _x0 = self._get_item_value(_row, 0)
            _roi['x0'] = int(_x0)

            _y0 = self._get_item_value(_row, 1)
            _roi['y0'] = int(_y0)

            _x1 = self._get_item_value(_row, 2)
            _roi['x1'] = int(_x1)

            _y1 = self._get_item_value(_row, 3)
            _roi['y1'] = int(_y1)

            x0_int = int(_x0)
            y0_int = int(_y0)
            width_int = np.abs(x0_int - int(_x1))
            height_int = np.abs(y0_int - int(_y1))

            _roi_id = self.init_roi(x0=x0_int, y0=y0_int,
                                    width=width_int, height=height_int)
            _roi['id'] = _roi_id
            list_roi[_row] = _roi

        self.list_roi = list_roi

        self.ui.table_roi.blockSignals(False)

        self.check_add_remove_button_widgets_status()

        if not _selection:
            _new_selection = QTableWidgetSelectionRange(0, 0, 0, 3)
            self.ui.table_roi.setRangeSelected(_new_selection, True)

    def init_roi(self, x0=0, y0=0, width=0, height=0):
        _color = QtGui.QColor(62, 13, 244)
        _pen = QtGui.QPen()
        _pen.setColor(_color)
        _pen.setWidthF(self.roi_width)
        _roi_id = pg.ROI([x0, y0], [width, height], pen=_pen, scaleSnap=True)
        _roi_id.addScaleHandle([1, 1], [0, 0])
        _roi_id.addScaleHandle([0, 0], [1, 1])
        self.ui.image_view.addItem(_roi_id)
        # add connection to roi
        _roi_id.sigRegionChanged.connect(self.roi_manually_moved)
        return _roi_id

    def check_add_remove_button_widgets_status(self):
        nbr_row = self.ui.table_roi.rowCount()
        if nbr_row > 0:
            self.ui.remove_roi_button.setEnabled(True)
        else:
            self.ui.remove_roi_button.setEnabled(False)

    def format_roi(self):
        roi_selected = {}
        for _key in self.list_roi.keys():
            _roi = self.list_roi[_key]
            x0 = _roi['x0']
            y0 = _roi['y0']
            x1 = _roi['x1']
            y1 = _roi['y1']
            new_entry = {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1}
            roi_selected[_key] = new_entry

        self.roi_selected = roi_selected

    def apply_clicked(self):
        self.update_table_roi(None) #check ROI before leaving application
        self.format_roi()
        self.close()

    def cancel_clicked(self):
        self.close()

    def closeEvent(self, eventhere=None):
        pass
