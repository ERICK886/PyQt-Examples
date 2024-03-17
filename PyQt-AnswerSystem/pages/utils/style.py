primary_100 = '#d4eaf7'
primary_200 = '#b6ccd8'
primary_300 = '#3b3c3d'
accent_100 = '#71c4ef'
accent_200 = '#00668c'
text_100 = '#1d1c1c'
text_200 = '#313d44'
bg_100 = '#fffefb'
bg_200 = '#f5f4f1'
bg_300 = '#cccbc8'

form_control = """
            QLineEdit {
                border: 1px solid #71c4ef;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                width: 100%;
                height: 100%;
                margin: 5px 5px 5px 5px;
            }
            
            QLineEdit:hover {
                border: 2px solid #71c4ef;
            }
            
            QLineEdit:focus {
                border: 2px solid #71c4ef 
            }
        """

btn_primary = """
            QPushButton {
                color: #fffefb;
                background-color: #00668c;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #71c4ef;
            }
        """

btn_danger = """
            QPushButton {
                color: #fffefb;
                background-color: #ff3333;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #ff6c6c
            }
        """

btn_secondary = """
            QPushButton {
                color: #fffefb;
                background-color: #3b3c3d;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #adacac;
            }
        """

btn_success = """
            QPushButton = {
                color: #22ad01;
                background-color: #1b6b01;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #7cff4f;
            }
        """

title_style = """
            QLabel {
                font-size: 35px;
                font-weight: bold;
                color: #3b3c3d;
                margin-bottom: 10px
            }
        """
h4 = """
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #3b3c3d;
                margin-bottom: 10px
            }
        """
radio_style = """
            QRadioButton {
                border-radius: 5px;
                font-size: 15px
            }
            
            QRadioButton:hover {
                color: #71c4ef;
            }
            
            QRadioButton:checked {
                color: #71c4ef;
            }
        """

check_style = """
            QCheckBox {
                border-radius: 5px;
                font-size: 15px
            }
            
            QCheckBox:hover {
                color: #71c4ef;
            }
            
            QCheckBox:checked {
                color: #71c4ef;
            }
        """
window_width = 1080
window_height = 640
