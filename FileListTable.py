#-*- coding: utf-8 -*-

import wx.grid as grid

class FileListGridTable(grid.GridTableBase):
	def __init__(self, datas):
		grid.GridTableBase.__init__(self)

		self.datas = datas

		self.colLabels = [u'File Name', u'File Path', u'Page Num']

		self.odd = grid.GridCellAttr()
		self.odd.SetReadOnly(True)
		self.odd.SetBackgroundColour('white')

		self.even = grid.GridCellAttr()
		self.even.SetReadOnly(True)

		pass

	def GetAttr(self, row, col, kind):
		attr = [self.even, self.odd][row % 2]
		attr.IncRef()
		return attr

	def GetNumberRows(self):
		return len(self.datas)

	def GetNumberCols(self):
		return len(self.colLabels)

	def GetColLabelValue(self, col):
		return self.colLabels[col]

	def GetRowLabelValue(self, row):
		return str(row)

	def GetValue(self, row, col):
		return self.datas[row][col]

	def ClearRows(self):
		self.DeleteRows(0, self.GetNumberRows())

	def RowMoveUp(self, row):
		if row > 0:
			temp = self.datas[row - 1]
			self.datas[row - 1] = self.datas[row]
			self.datas[row] = temp
			
			self.isModified = True

	def RowMoveDown(self, row):
		if row < self.GetNumberRows():
			temp = self.datas[row + 1]
			self.datas[row + 1] = self.datas[row]
			self.datas[row] = temp
			
			self.isModified = True

	
	def AppendRows(self, newData=None):		
		self.datas.append(newData)
		self.isModified = True
		gridView = self.GetView()
		gridView.BeginBatch()
		appendMsg = grid.GridTableMessage(self, grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
		gridView.ProcessTableMessage(appendMsg)
		gridView.EndBatch()
		getValueMsg = grid.GridTableMessage(self, grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
		gridView.ProcessTableMessage(getValueMsg)
	
		return True

	def SetValue(self, row, col, value):
		try:
			self.datas[row][col] = value
		except IndexError:
			# add a new row
			self.datas.append([''] * self.GetNumberCols())
			innerSetValue(row, col, value)
	
			# tell the grid we've added a row
			msg = grid.GridTableMessage(self,  # The table
										grid.GRIDTABLE_NOTIFY_ROWS_APPENDED,  # what we did to it
										1  # how many
										)
	
			self.GetView().ProcessTableMessage(msg)
	
	def DeleteRows(self, pos=0, numRows=0):
		if self.datas is None or len(self.datas) == 0 or numRows == 0:
			return False

		del self.datas[pos:numRows]
	
		gridView = self.GetView()
		gridView.BeginBatch()
		deleteMsg = grid.GridTableMessage(self, grid.GRIDTABLE_NOTIFY_ROWS_DELETED, pos, numRows)
		gridView.ProcessTableMessage(deleteMsg)
		gridView.EndBatch()
		getValueMsg = grid.GridTableMessage(self, grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
		gridView.ProcessTableMessage(getValueMsg)

		self.isModified = True
	
		return True