from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    
    # authenticated = QtCore.pyqtSignal()
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(252, 123)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.username_edit = QtWidgets.QLineEdit(Form)
        self.username_edit.setObjectName("username_edit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.username_edit)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.password_edit = QtWidgets.QLineEdit(Form)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.setObjectName("password_edit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.password_edit)
        self.submit_btn = QtWidgets.QPushButton(Form)
        self.submit_btn.setObjectName("submit_btn")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.submit_btn)
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setObjectName("checkBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.checkBox)

        # self.submit_btn.clicked.connect(self.authenticate)
        
        self.retranslateUi(Form) # <-이 함
        self.label.setText(("Login to cool Application"))
        self.label_3.setText(( "User"))
        self.label_2.setText(("비밀번호"))
        self.submit_btn.setText(( "Login"))
        self.checkBox.setText(("I agree to the legalese"))
        
        QtCore.QMetaObject.connectSlotsByName(Form)
 
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Login to cool Application"))
        self.label_3.setText(_translate("Form", "User"))
        self.label_2.setText(_translate("Form", "비밀번호"))
        self.submit_btn.setText(_translate("Form", "Login"))
        self.checkBox.setText(_translate("Form", "I agree to the legalese"))

    # def authenticate(self):
    #     username=self.username_edit.text()
    #     password=self.password_edit.text()
    #     if username=='user' and password=="pass":
    #         #self.authenticated.emit()
    #         QtWidgets.QMessageBox.information(None, 'Success', 'You logged in, bro or sis.')
    #     else:
    #         QtWidgets.QMessageBox.critical(None, 'Fail', "No logged for you")
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
