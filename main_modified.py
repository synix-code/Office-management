# importing the important library
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition, FadeTransition
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.toast import toast
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.snackbar import Snackbar
import re
from kivy.utils import get_color_from_hex
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint
import config  # Import your credentials
import threading  # For running the email task in a separate thread
import time
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
import firebase_admin
from firebase_admin import credentials, firestore
import json
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import ThreeLineListItem
import os
import sys
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.label import MDLabel










# Defining the window size just for testing
Window.size = (300,600)


class NavBar(FakeRectangularElevationBehavior, FloatLayout):
    pass
class Navigation(FakeRectangularElevationBehavior, FloatLayout):
    pass
class Navigationb(FakeRectangularElevationBehavior, FloatLayout):
    pass
class Navigationba(FakeRectangularElevationBehavior, FloatLayout):
    pass
class Navigationbar(FakeRectangularElevationBehavior, FloatLayout):
    pass



# defining the screen classes for the KV screens 
class SplashScreen(Screen):
    # this function wil call at enter on screen automatically
    def on_enter(self):
        # Snackbar(text="Hello sir", duration=2).open()
        # Snackbar(txt = "Single-line snackbar").open()
        global scr
        scr = []
        # this line will call the function after 8 seconds using clock property 
        Clock.schedule_once(self.switch_screen, 8)


    def switch_screen(self, dt):
        try:
            with open("user_data.json", "r") as json_file:
                data = json.load(json_file)

            comp = data.get("comp")
            owner = data.get("owner")
            email = data.get("email")
            pswd = data.get("pswd")

            print(comp, owner, email, pswd)

            # Output print karne ke liye
            print("JSON file ka data:")
            print(json.dumps(data, indent=4))
            # this will change the transition to no transition from slide transition 
            self.manager.transition = NoTransition()
            # change screen to the login screen 
            self.manager.current = "home"

        except:
            # this will change the transition to no transition from slide transition 
            self.manager.transition = NoTransition()
            # change screen to the login screen 
            self.manager.current = "login"

class LoginScreen(Screen):
    pass

class SignupScreen(Screen):
    pass

class MainScreen(Screen):
    def on_enter(self):  # Call this method when MainScreen is entered
        thread = threading.Thread(target=self.load_employee_data)
        thread.start()

    def load_employee_data(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("office-hub.json")
            firebase_admin.initialize_app(cred)

        with open("user_data.json", "r") as f:
            data = json.load(f)
        email = data.get("email")

        db = firestore.client()
        doc_ref = db.collection("users").document(email)
        doc = doc_ref.get()

        if doc.exists:
            user_data = doc.to_dict()

            # Prepare employee list
            self.employee_details = []

            try:

                for key, val in user_data.items():
                    if key.startswith("employee.") and isinstance(val, dict):
                        name = key.split("employee.")[1]
                        role = val.get("role", "N/A")
                        salary = val.get("salary", "N/A")
                        self.employee_details.append((name, role, salary))
            except Exception as e:
                print(e)

            Clock.schedule_once(self.populate_main_list)

    def populate_main_list(self, dt):
        self.ids.main_list.clear_widgets()

        try:

            if not self.employee_details:
                self.ids.main_list.add_widget(
                    MDLabel(
                        text="Your employee list is empty.\nPlease add employee from profile screen.",
                        halign="center",
                        # theme_text_color="Hint"
                    )
                )
                self.ids.home_spinner.active = False
                return
            else:

                for name, role, salary in self.employee_details:
                    item = ThreeLineListItem(
                        text=name,
                        secondary_text=f"Role: {role}",
                        tertiary_text=f"Salary: ₹{salary}"
                    )
                    self.ids.main_list.add_widget(item)
                item_empty = ThreeLineListItem(
                    text="",
                    secondary_text="",
                    tertiary_text=""
                )
                self.ids.main_list.add_widget(item_empty)
                self.ids.home_spinner.active = False
        except Exception as e:
            print(e)

class EntryScreen(Screen):
    pass

class AttendenceScreen(Screen):
    pass

class ViewScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class InWardScreen(Screen):
    pass

class OutWardScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

class EmployeeFormScreen(Screen):
    pass
class AboutAppScreen(Screen):
    pass
class AboutDevScreen(Screen):
    pass

class ThemeScreen(Screen):
    pass

class FillAttendenceScreen(Screen):
    pass

class FillDepAttendenceScreen(Screen):
    pass


class ArrivalScreen(Screen):
    def on_enter(self):  # Call this method when MainScreen is entered
        thread = threading.Thread(target=self.load_employee_data)
        thread.start()

    def load_employee_data(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("office-hub.json")
            firebase_admin.initialize_app(cred)

        with open("user_data.json", "r") as f:
            data = json.load(f)
        email = data.get("email")

        db = firestore.client()
        doc_ref = db.collection("users").document(email)
        doc = doc_ref.get()

        if doc.exists:
            user_data = doc.to_dict()

            # Prepare employee list
            self.employee_details = []

            try:

                for key, val in user_data.items():
                    if key.startswith("employee.") and isinstance(val, dict):
                        name = key.split("employee.")[1]
                        role = val.get("role", "N/A")
                        salary = val.get("salary", "N/A")
                        self.employee_details.append((name, role, salary))
            except Exception as e:
                print(e)

            Clock.schedule_once(self.populate_main_list)

    def populate_main_list(self, dt):
        self.ids.arrival_list.clear_widgets()

        try:

            if not self.employee_details:
                self.ids.arrival_list.add_widget(
                    MDLabel(
                        text="Your employee list is empty.\nPlease add employee from profile screen.",
                        halign="center",
                        theme_text_color="Hint"
                    )
                )
                self.ids.arrival_spinner.active = False
                return
                for name, role, salary in self.employee_details:
                    item = TwoLineListItem(
                        text=name,
                        secondary_text=f"Role: {role}"
                    )
                    # Extra data assign karne ka option (if needed later)
                    item.role = role
                    item.salary = salary

                    # Correct binding
                    item.bind(on_release=self.item_clicked)

                    self.ids.arrival_list.add_widget(item)

                # Extra empty item at the end
                item_empty = TwoLineListItem(
                    text="",
                    secondary_text=""
                )
                self.ids.arrival_list.add_widget(item_empty)

                self.ids.arrival_spinner.active = False

        except Exception as e:
            print(e)

    def item_clicked(self, instance):
        print(f"Clicked Employee Name: {instance.text}")

        self.manager.current = "fillatt"
        fillatt_screen = self.manager.get_screen("fillatt")
        fillatt_screen.ids.user_att.text = instance.text

        # self.ids.user_att.text = instance.text



class DepartureScreen(Screen):
    def on_enter(self):  # Call this method when MainScreen is entered
        thread = threading.Thread(target=self.load_employee_data)
        thread.start()

    def load_employee_data(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("office-hub.json")
            firebase_admin.initialize_app(cred)

        with open("user_data.json", "r") as f:
            data = json.load(f)
        email = data.get("email")

        db = firestore.client()
        doc_ref = db.collection("users").document(email)
        doc = doc_ref.get()

        if doc.exists:
            user_data = doc.to_dict()

            # Prepare employee list
            self.employee_details = []

            try:

                for key, val in user_data.items():
                    if key.startswith("employee.") and isinstance(val, dict):
                        name = key.split("employee.")[1]
                        role = val.get("role", "N/A")
                        salary = val.get("salary", "N/A")
                        self.employee_details.append((name, role, salary))
            except Exception as e:
                print(e)

            Clock.schedule_once(self.populate_main_list)

    def populate_main_list(self, dt):
        self.ids.departure_list.clear_widgets()

        try:

            if not self.employee_details:
                self.ids.departure_list.add_widget(
                    MDLabel(
                        text="Your employee list is empty.\nPlease add employee from profile screen.",
                        halign="center",
                        theme_text_color="Hint"
                    )
                )
                self.ids.departure_spinner.active = False
                return
                for name, role, salary in self.employee_details:
                    item = TwoLineListItem(
                        text=name,
                        secondary_text=f"Role: {role}"
                    )
                    # Extra data assign karne ka option (if needed later)
                    item.role = role
                    item.salary = salary

                    # Correct binding
                    item.bind(on_release=self.item_clicked)

                    self.ids.departure_list.add_widget(item)

                # Extra empty item at the end
                item_empty = TwoLineListItem(
                    text="",
                    secondary_text=""
                )
                self.ids.departure_list.add_widget(item_empty)

                self.ids.departure_spinner.active = False

        except Exception as e:
            print(e)

    def item_clicked(self, instance):
        print(f"Clicked Employee Name: {instance.text}")

        self.manager.current = "fillattdep"
        fillatt_screen = self.manager.get_screen("fillattdep")
        fillatt_screen.ids.user_att_dep.text = instance.text

        # self.ids.user_att.text = instance.text

# main app class 
class MyApp(MDApp):
    def build(self):
        # defining the app title manually
        self.title = "Office Management"
        # defining the icon manually
        self.icon = "images/logo.png"
        # loading the kv file via a Builder property 
        self.bldr = Builder.load_file("main.kv")

        self.bldr.bind(current=self.on_screen_change)
        # binding keyboard to the screen 
        Window.bind(on_keyboard=self.on_keyboard)
        return self.bldr
    
    # def on_start(self):
    #     self.bldr.get_screen("fillattdep").manager.current = "fillattdep"

    def on_screen_change(self, instance, value):
        try:
            # print("Hello World")
            current_scr = self.root.current
            print(current_scr)
            if current_scr not in scr:
                scr.append(current_scr)
            else:
                scr.pop()
            print(scr)
        except:
            toast("This is a toast message!")

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        print(f"Key: {key}, Scancode: {scancode}")
        # 27 = Escape key (Desktop), 1001 = Android back button, 4 = Android back
        if key in (27, 1001, 4):
            current = self.root.current
            print(f"Back pressed. Current screen: {current}")

            if current not in ["splash", "login", "home"]:

                print(scr)
                now = scr[-2]
                self.root.transition.direction = "right"
                self.root.current = now
                # Go back to previous screen
                # previous = self.screen_history[-1] if self.screen_history else "splash"
                # self.root.current = previous
                return True  # Handled
        return False  # Let system handle

    
    # defining the class for go to signup screen 
    def signup(self):
        # changing the transition 
        self.bldr.get_screen("login").manager.transition = SlideTransition()
        # setting the direction for transition 
        self.bldr.get_screen("login").manager.transition.direction = "left"
        # changing the screen to the signup screen 
        self.bldr.get_screen("login").manager.current = "signup"

    # go back to the login screen from signup screen 
    def go_back(self):
        # setting the direction for transition 
        self.bldr.get_screen("signup").manager.transition.direction = "right"
        # changing the screen to the signup screen 
        self.bldr.get_screen("signup").manager.current = "login"

    # password show hide system 
    def password_show_hide(self):
        screen = self.bldr.get_screen("login")
        field = screen.ids.eye_btn
        change = screen.ids.change_eye
        if field.password == True:
            field.password = False
            change.icon = "eye-off"
        else:
            field.password = True
            change.icon = "eye"

    

    def check_comp(self):
        comp = self.bldr.get_screen("signup").ids.company_name.text
        if comp.strip() == "":
            self.bldr.get_screen("signup").ids.company_name.error = True
            self.bldr.get_screen("signup").ids.company_name.helper_text = "Please Enter a vaild Name"
        elif len(comp.strip()) <= 4:
            self.bldr.get_screen("signup").ids.company_name.error = True
            self.bldr.get_screen("signup").ids.company_name.helper_text = "Company name must be 5 Contains"

        else:
            self.bldr.get_screen("signup").ids.company_name.helper_text = ""
    def check_owner(self):
        owner = self.bldr.get_screen("signup").ids.owner_name.text
        if owner.strip() == "":
            self.bldr.get_screen("signup").ids.owner_name.error = True
            self.bldr.get_screen("signup").ids.owner_name.helper_text = "Please Enter a vaild Name"
        
        elif len(owner.strip()) <= 2:
            self.bldr.get_screen("signup").ids.owner_name.error = True
            self.bldr.get_screen("signup").ids.owner_name.helper_text = "Owner name must be 3 Contains"

        else:
            self.bldr.get_screen("signup").ids.owner_name.helper_text = ""


    def check_email(self):
        email = self.bldr.get_screen("signup").ids.email.text.strip()
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if email == "":
            self.bldr.get_screen("signup").ids.email.error = True
            self.bldr.get_screen("signup").ids.email.helper_text = "Please enter your email"
        elif not re.match(pattern, email):
            self.bldr.get_screen("signup").ids.email.error = True
            self.bldr.get_screen("signup").ids.email.helper_text = "Enter a valid email address"
        else:
            self.bldr.get_screen("signup").ids.email.error = False
            self.bldr.get_screen("signup").ids.email.helper_text = ""

    def check_otp(self):
        otp = self.bldr.get_screen("signup").ids.otp.text
        if otp.strip() == "":
            self.bldr.get_screen("signup").ids.otp.error = True
            self.bldr.get_screen("signup").ids.otp.helper_text = "Please Enter OTP"
        elif len(otp.strip()) >= 7 or len(otp.strip()) < 6:
            self.bldr.get_screen("signup").ids.otp.error = True
            self.bldr.get_screen("signup").ids.otp.helper_text = "OTP must be 6 Contains."
        else:
            self.bldr.get_screen("signup").ids.otp.error = False
            self.bldr.get_screen("signup").ids.otp.helper_text = ""

    def check_password(self):
        pswd1 = self.bldr.get_screen("signup").ids.password.text.strip()
        password_field = self.bldr.get_screen("signup").ids.password

        # Empty check
        if pswd1 == "":
            password_field.error = True
            password_field.helper_text = "Password cannot be empty"
        # Length check
        elif len(pswd1) < 6:
            password_field.error = True
            password_field.helper_text = "Password must be at least 6 characters"
        # Space check
        elif " " in pswd1:
            password_field.error = True
            password_field.helper_text = "Password cannot contain spaces"
        # Uppercase check
        elif not re.search(r"[A-Z]", pswd1):
            password_field.error = True
            password_field.helper_text = "Must include at least 1 uppercase letter"
        # Lowercase check
        elif not re.search(r"[a-z]", pswd1):
            password_field.error = True
            password_field.helper_text = "Must include at least 1 lowercase letter"
        # Digit check
        elif not re.search(r"[0-9]", pswd1):
            password_field.error = True
            password_field.helper_text = "Must include at least 1 number"
        # Special character check
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pswd1):
            password_field.error = True
            password_field.helper_text = "Must include at least 1 special character"
        else:
            password_field.error = False
            password_field.helper_text = ""

    def check_password_con(self):
        pswd1 = self.bldr.get_screen("signup").ids.password.text.strip()
        pswd2 = self.bldr.get_screen("signup").ids.confirm_password.text.strip()
        if pswd2 == "":
            self.bldr.get_screen("signup").ids.confirm_password.error = True
            self.bldr.get_screen("signup").ids.confirm_password.helper_text = "Please Confirm your Password"

        elif pswd2 != pswd1:
            self.bldr.get_screen("signup").ids.confirm_password.error = True
            self.bldr.get_screen("signup").ids.confirm_password.helper_text = "Your password didn't match"

        else:
            self.bldr.get_screen("signup").ids.confirm_password.error = False
            self.bldr.get_screen("signup").ids.confirm_password.helper_text = ""

    def send_mail(self):
        # check the require
        self.check_email()
        if self.bldr.get_screen("signup").ids.email.error == False:
            self.bldr.get_screen("signup").ids.send_mail.disabled = True
            email_thread = threading.Thread(target=self.email_task)
            email_thread.start()
            # email_thread.join()

    def email_task(self):
        # self.dialog = None
        # Generate 6-digit OTP
        global r_otp
        r_otp = str(randint(100000, 999999))

        # Load HTML template and inject OTP
        with open("otp.html", "r", encoding="utf-8") as file:
            html_template = file.read()

        html_content = html_template.replace("{{ OTP_CODE }}", r_otp)

        # Email setup
        sender_email = config.Email
        sender_password = config.Password
        receiver_email = self.bldr.get_screen("signup").ids.email.text

        # Create the email
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your OTP Code"
        message["From"] = sender_email
        message["To"] = receiver_email
        message.attach(MIMEText(html_content, "html"))

        # Send the email
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            print(f"OTP {r_otp} sent to {receiver_email}")
            try:
                if not firebase_admin._apps:
                    # Replace with your Firebase service account key file
                    cred = credentials.Certificate("office-hub.json")
                    firebase_admin.initialize_app(cred)

                # Initialize Firestore DB
                db = firestore.client()

                # Reference to 'users' collection
                users_ref = db.collection('users')

                # Get all documents
                docs = users_ref.stream()
                global all_emails
                all_emails = []
                # Print all document IDs (email IDs)
                print("All emails (document IDs):")
                for doc in docs:
                    all_emails.append(doc.id)
                    # print(doc.id)  # This will print all email addresses (document IDs)

                print(all_emails)
            except Exception as e:
                print(e)
            self.bldr.get_screen("signup").ids.request.disabled = False
            # Clock.schedule_once(lambda dt: self.dialog_md(receiver_email), 0)
            Clock.schedule_once(lambda dt: self.dialog_md(receiver_email), 0)
            # self.dialog_md(self)
            

            # time.sleep(27)

            self.bldr.get_screen("signup").ids.send_mail.font_name = "fnt/shimosa.regular.ttf"
            self.bldr.get_screen("signup").ids.send_mail.font_size = "22sp"
            self.bldr.get_screen("signup").ids.send_mail.text = "27"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "26"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "25"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "24"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "23"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "22"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "21"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "20"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "19"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "18"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "17"
            
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "16"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "15"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "14"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "13"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "12"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "11"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "10"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "9"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "8"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "7"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "6"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "5"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "4"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "3"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "2"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "1"
            time.sleep(1)
            self.bldr.get_screen("signup").ids.send_mail.text = "0"
            time.sleep(0)
            self.bldr.get_screen("signup").ids.send_mail.text = "Send OTP"
            self.bldr.get_screen("signup").ids.send_mail.disabled = False
            self.bldr.get_screen("signup").ids.send_mail.font_name = "fnt/horror-Origins-demo.ttf"
            self.bldr.get_screen("signup").ids.send_mail.font_size = "10sp"
            self.bldr.get_screen("signup").ids.send_mail.text = "Resend"
            self.bldr.get_screen("signup").ids.send_mail.color = (1,0,0,1)
            # email_thread.join()
            

        except Exception as e:
            Clock.schedule_once(lambda dt: self.otp_fail(), 0)
            # self.otp_fail(e)

    def otp_fail(self, dt=None):
        self.dialog = MDDialog(
            title="Error Sending mail.",
            text=f"Please check your conection",
            size_hint=(0.8, None),
                # buttons=[
                #     MDRaisedButton(
                #         text="OK",
                #         on_release=lambda x: self.dialog.dismiss(),
                #         color = "FF69B4"
                #     ),
                # ],
        )
        self.dialog.open()
        self.bldr.get_screen("signup").ids.send_mail.disabled = False

    def dialog_md(self, receiver_email):
        # self.dialog = None
        self.dialog = MDDialog(
            title="OTP Sent Successfully.",
            text=f"An OTP has been sent to:\n[b]{receiver_email}[/b]",
            size_hint=(0.8, None),
            # buttons=[
            #     MDRaisedButton(
            #         text="OK",
            #         on_release=lambda x: self.dialog.dismiss(),
            #         color = "FF69B4"
            #     ),
            # ],
        )
        self.dialog.text = f"An OTP has been sent to:\n[b]{receiver_email}[/b]"
        self.dialog.text = f"An OTP has been sent to:\n[b]{receiver_email}[/b]"
        self.dialog.open()

    

    # validation of creating account
    def validate_signup(self):
        comp = self.bldr.get_screen("signup").ids.company_name.text.strip()
        owner = self.bldr.get_screen("signup").ids.owner_name.text.strip()
        email = self.bldr.get_screen("signup").ids.email.text.strip()
        otp = self.bldr.get_screen("signup").ids.otp.text.strip()
        pswd1 = self.bldr.get_screen("signup").ids.password.text.strip()
        pswd2 = self.bldr.get_screen("signup").ids.confirm_password.text.strip()

        has_error = False


        
        try:

            # Company Name Check
            if comp == "" or len(comp) <= 4:
                self.bldr.get_screen("signup").ids.company_name.error = True
                self.bldr.get_screen("signup").ids.company_name.helper_text = "Company name must be at least 5 characters"
                has_error = True
            else:
                self.bldr.get_screen("signup").ids.company_name.error = False
                self.bldr.get_screen("signup").ids.company_name.helper_text = ""

            # Owner Name Check
            if owner == "" or len(owner) <= 2:
                self.bldr.get_screen("signup").ids.owner_name.error = True
                self.bldr.get_screen("signup").ids.owner_name.helper_text = "Owner name must be at least 3 characters"
                has_error = True
            else:
                self.bldr.get_screen("signup").ids.owner_name.error = False
                self.bldr.get_screen("signup").ids.owner_name.helper_text = ""

            # Email Check
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if email == "" or not re.match(pattern, email):
                self.bldr.get_screen("signup").ids.email.error = True
                self.bldr.get_screen("signup").ids.email.helper_text = "Enter a valid email address"
                has_error = True
            elif email in all_emails:
                self.bldr.get_screen("signup").ids.email.text = ""
                self.bldr.get_screen("signup").ids.otp.text = ""
                self.bldr.get_screen("signup").manager.transition = NoTransition()
                self.bldr.get_screen("signup").manager.current = "login"
                self.dialog = MDDialog(
                    title="This Email is already exist!",
                    text=f"{email} is already exist please login or try diffrence email.",
                    size_hint=(0.8, None),
                        # buttons=[
                        #     MDRaisedButton(
                        #         text="OK",
                        #         on_release=lambda x: self.dialog.dismiss(),
                        #         color = "FF69B4"
                        #     ),
                        # ],
                )
                self.dialog.open()
                has_error = True
            else:
                self.bldr.get_screen("signup").ids.email.error = False
                self.bldr.get_screen("signup").ids.email.helper_text = ""

            # OTP Check
            if otp == "" or len(otp) != 6 or not otp.isdigit():
                self.bldr.get_screen("signup").ids.otp.error = True
                self.bldr.get_screen("signup").ids.otp.helper_text = "OTP must be 6 digits"
                has_error = True
            elif otp != str(r_otp):
                self.bldr.get_screen("signup").ids.otp.error = True
                self.bldr.get_screen("signup").ids.otp.helper_text = "Wrong OTP. Please try again."
                has_error = True
            else:
                self.bldr.get_screen("signup").ids.otp.error = False
                self.bldr.get_screen("signup").ids.otp.helper_text = ""

            # Password Check
            if pswd1 == "":
                self.bldr.get_screen("signup").ids.password.error = True
                self.bldr.get_screen("signup").ids.password.helper_text = "Password cannot be empty"
                has_error = True
            elif len(pswd1) < 6:
                self.bldr.get_screen("signup").ids.password.error = True
                self.bldr.get_screen("signup").ids.password.helper_text = "Password must be at least 6 characters"
                has_error = True
            else:
                self.bldr.get_screen("signup").ids.password.error = False
                self.bldr.get_screen("signup").ids.password.helper_text = ""

            # Confirm Password Check
            if pswd2 == "":
                self.bldr.get_screen("signup").ids.confirm_password.error = True
                self.bldr.get_screen("signup").ids.confirm_password.helper_text = "Please confirm your password"
                has_error = True
            elif pswd1 != pswd2:
                self.bldr.get_screen("signup").ids.confirm_password.error = True
                self.bldr.get_screen("signup").ids.confirm_password.helper_text = "Passwords do not match"
                has_error = True
            else:
                self.bldr.get_screen("signup").ids.confirm_password.error = False
                self.bldr.get_screen("signup").ids.confirm_password.helper_text = ""

            if not has_error:
                print("✅ All fields valid, proceed to create account")
                # Continue to account creation logic
                # email_thread = threading.Thread(target=self.email_task)
                # email_thread.start()
                # threading.Thread(target=self.email_task).join()
                # Create and start thread
                Clock.schedule_once(lambda dt: self.start_storing_thread(), 0)
                
                # self.store_data(comp, owner, email, pswd1)
        except Exception as e:
            print(e)


    


    def start_storing_thread(self, dt=None):
        Clock.schedule_once(lambda dt: self.on_spinner())
        

    def on_spinner(self, dt=None):
        comp = self.bldr.get_screen("signup").ids.company_name.text.strip()
        owner = self.bldr.get_screen("signup").ids.owner_name.text.strip()
        email = self.bldr.get_screen("signup").ids.email.text.strip()
        pswd1 = self.bldr.get_screen("signup").ids.password.text.strip()
        main_content = self.bldr.get_screen("signup").ids.all_widget
        for child in main_content.children:
            try:
                child.disabled = True  # Disable each widget
            except Exception as e:
                print(f"Error disabling {child}: {e}")

        self.bldr.get_screen("signup").ids.sign_spinner.active = True
        storage_thread = threading.Thread(
            target=self.store_data,
            args=(comp, owner, email, pswd1),
            daemon=True  # Ensures thread exits when app closes
        )
        storage_thread.start()

    def store_data(self, comp, owner, email, pswd1):
        try:
            # Initialize Firebase in background thread
            if not firebase_admin._apps:
                cred = credentials.Certificate("office-hub.json")
                firebase_admin.initialize_app(cred)
            
            db = firestore.client()
            user_ref = db.collection("users").document(email)
            
            user_ref.set({
                "email": email,
                "company_name": comp,
                "owner_name": owner,
                "password": pswd1,  # T Hash this password!
            }, merge=True)
            
            # Update UI in main thread after completion
            Clock.schedule_once(lambda dt: self.on_storage_success(email, comp, owner, pswd1))
            
        except Exception as e:
            print((str(e)))
            Clock.schedule_once(lambda dt: self.on_storage_error())


    def on_storage_error(self, dt=None):
        self.dialog = MDDialog(
            title="Account creation Failed!",
            text=f"Account creation failed. please check your connection",
            size_hint=(0.8, None),
                # buttons=[
                #     MDRaisedButton(
                #         text="OK",
                #         on_release=lambda x: self.dialog.dismiss(),
                #         color = "FF69B4"
                #     ),
                # ],
        )
        self.dialog.open()
        main_content = self.bldr.get_screen("signup").ids.all_widget
        self.bldr.get_screen("signup").ids.sign_spinner.active = False
        for child in main_content.children:
            try:
                child.disabled = False
            except Exception as e:
                print(f"Error disabling {child}: {e}")
            

    def on_storage_success(self, email, comp, owner, pswd1):
        data = {
            "comp": comp,
            "owner": owner,
            "email": email,
            "pswd": pswd1
        }
        # Save the data to a JSON file
        with open("user_data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        print("JSON file created successfully!")

        self.bldr.get_screen("home").manager.transition = NoTransition()
        self.bldr.get_screen("home").manager.current = "home"  # Switch to main screen
        self.dialog = MDDialog(
            title="Account creation Complete",
            text=f"Your account has been created with {email}",
            size_hint=(0.8, None),
                # buttons=[
                #     MDRaisedButton(
                #         text="OK",
                #         on_release=lambda x: self.dialog.dismiss(),
                #         color = "FF69B4"
                #     ),
                # ],
        )
        self.dialog.open()
        # toast(f"Account created for {email}")

    def login_clicked(self):
        login_thread = threading.Thread(target=self.login_test)
        login_thread.start()

    def login_test(self):
        email = self.bldr.get_screen("login").ids.email_log.text.strip()
        password1 = self.bldr.get_screen("login").ids.eye_btn.text.strip()
        error = False
        self.bldr.get_screen("login").ids.login_spinner.active = True

        try:
            if not firebase_admin._apps:
                # Replace with your Firebase service account key file
                cred = credentials.Certificate("office-hub.json")
                firebase_admin.initialize_app(cred)

            # Initialize Firestore DB
            db = firestore.client()

            # Reference to 'users' collection
            users_ref = db.collection('users')

            # Get all documents
            docs = users_ref.stream()
            global all_emails
            all_emails = []
            # Print all document IDs (email IDs)
            print("All emails (document IDs):")
            for doc in docs:
                all_emails.append(doc.id)
                # print(doc.id)  # This will print all email addresses (document IDs)

            print(all_emails)
            db = firestore.client()
        
                # Specific user का document reference
            user_ref = db.collection("users").document(email)
                
                # Document fetch करें
            doc = user_ref.get()
                
                # Check करें कि document exists है
            if doc.exists:
                    # Document data को dictionary में प्राप्त करें
                user_data = doc.to_dict()
                    
                    # Password field access करें
                password = user_data.get("password")
                    
                print(f"User Password: {password}")
                # return password
            else:
                print("User document does not exist")
                # return None
        except Exception as e:
            print(e)


        if email == "":
            self.bldr.get_screen("login").ids.email_log.error = True
            self.bldr.get_screen("login").ids.email_log.helper_text = "Please Enter a vaild email"
            error == True
            self.bldr.get_screen("login").ids.login_spinner.active = False
        elif email not in all_emails:
            self.bldr.get_screen("login").ids.email_log.error = True
            self.bldr.get_screen("login").ids.email_log.helper_text = "This Email is not Exist"
            error == True
            self.bldr.get_screen("login").ids.login_spinner.active = False
        else:
            self.bldr.get_screen("login").ids.email_log.error = False
            self.bldr.get_screen("login").ids.email_log.helper_text = ""
            error == False

        if password1 == "":
            self.bldr.get_screen("login").ids.eye_btn.error = True
            self.bldr.get_screen("login").ids.eye_btn.helper_text = "Please Enter a password first."
            error == True
            self.bldr.get_screen("login").ids.login_spinner.active = False
        elif password1 != password:
            self.bldr.get_screen("login").ids.eye_btn.error = True
            self.bldr.get_screen("login").ids.eye_btn.helper_text = "Your password didn't match."
            error == True
            self.bldr.get_screen("login").ids.login_spinner.active = False
        else:
            self.bldr.get_screen("login").ids.eye_btn.error = False
            self.bldr.get_screen("login").ids.eye_btn.helper_text = ""
            error == False
            self.bldr.get_screen("login").ids.login_spinner.active = True
            try:
                # User document fetch करें
                user_ref = db.collection("users").document(email)
                doc = user_ref.get()
                
                if doc.exists:
                    # सारे data को dictionary में प्राप्त करें
                    user_data = doc.to_dict()
                    
                    # अलग-अलग variables में store करें
                    user_email = doc.id  # Document ID (email)
                    company_name = user_data.get("company_name", "")
                    owner_name = user_data.get("owner_name", "")
                    user_password = user_data.get("password", "")  # Note: यह hashed होना चाहिए
                    registration_date = user_data.get("registration_date", "")
                    account_status = user_data.get("status", "active")
                    
                    # Debugging के लिए print करें
                    print("\nStored User Data:")
                    print(f"Email: {user_email}")
                    print(f"Company: {company_name}")
                    print(f"Owner: {owner_name}")
                    print(f"Password Hash: {user_password}")
                    print(f"Registration Date: {registration_date}")
                    print(f"Account Status: {account_status}")

                    data = {
                        "comp": company_name,
                        "owner": owner_name,
                        "email": user_email,
                        "pswd": user_password
                    }
                    # Save the data to a JSON file
                    with open("user_data.json", "w") as json_file:
                        json.dump(data, json_file, indent=4)

                    print("JSON file created successfully!")
                    self.bldr.get_screen("login").ids.login_spinner.active = False
                    Clock.schedule_once(lambda dt: self.login_main(), 0)
                    
                    
                    return True
                else:
                    print("User document does not exist")
                    return False
                    
            except Exception as e:
                print(f"Error fetching user data: {e}")
                return False
            
    def login_main(self, dt=None):
        self.bldr.get_screen("login").manager.current = "home"
            





    def check_mail_exist(self):
        pass


    def home_screen(self):
        print("clicked")
        self.bldr.get_screen("home").manager.transition = NoTransition()
        self.bldr.get_screen("home").manager.current = "home"



    def entry_screen(self):
        print("clicked")
        self.bldr.get_screen("entry").manager.transition = NoTransition()
        self.bldr.get_screen("entry").manager.current = "entry"

    def attendence_screen(self):
        print("clicked")
        self.bldr.get_screen("attendence").manager.transition = NoTransition()
        self.bldr.get_screen("attendence").manager.current = "attendence"

    def view_screen(self):
        print("clicked")
        self.bldr.get_screen("view").manager.transition = NoTransition()
        self.bldr.get_screen("view").manager.current = "view"


    def settings_screen(self):
        print("clicked")
        self.bldr.get_screen("settings").manager.transition = NoTransition()
        self.bldr.get_screen("settings").manager.current = "settings"

    
    def profile_screen(self):
        thread = threading.Thread(
            target=self.count_employee,
            daemon=True
        )
        thread.start()

        self.bldr.get_screen("profile").manager.transition = NoTransition()
        self.bldr.get_screen("profile").manager.current = "profile"

        with open("user_data.json", "r") as file:
            data = json.load(file)

        name = data.get("owner")
        self.bldr.get_screen("profile").ids.dummy.text = name

    # Update GUI after thread completes
    def update_employee_count(self, dt):
        try:
            count = len(self.employee_names)
            self.bldr.get_screen("profile").ids.emp_count.text = str(count)
        except Exception as e:
            print(e)

    def count_employee(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("office-hub.json")
            firebase_admin.initialize_app(cred)

        with open("user_data.json", "r") as f:
            data = json.load(f)
        email = data.get("email")

        db = firestore.client()
        doc_ref = db.collection("users").document(email)
        doc = doc_ref.get()

        self.employee_names = []

        if doc.exists:
            user_data = doc.to_dict()
            try:
                for key in user_data.keys():
                    if key.startswith("employee."):
                        name = key.split("employee.")[1]
                        self.employee_names.append(name)
            except exception as e:
                print(e)

            print("✅ Employee Names:", self.employee_names)

            # Call UI update safely
            Clock.schedule_once(self.update_employee_count)

        else:
            print("❌ No document found.")



    def employee_form_screen(self):
        self.bldr.get_screen("employeeform").manager.transition = NoTransition()
        self.bldr.get_screen("employeeform").manager.current = "employeeform"


    def add_emp_db(self):
        emp_name = self.bldr.get_screen("employeeform").ids.emp_name.text
        emp_role = self.bldr.get_screen("employeeform").ids.emp_role.text
        emp_salary = self.bldr.get_screen("employeeform").ids.emp_salary.text
        with open("user_data.json", "r") as file:
            data = json.load(file)

        email = data.get("email")


        if emp_name.strip() == "":
            self.bldr.get_screen("employeeform").ids.emp_name.error = True
        else:
            self.bldr.get_screen("employeeform").ids.emp_name.error = False

        if emp_role.strip() == "":
            self.bldr.get_screen("employeeform").ids.emp_role.error = True
        else:
            self.bldr.get_screen("employeeform").ids.emp_role.error = False

        if emp_salary.strip() == "":
            self.bldr.get_screen("employeeform").ids.emp_salary.error = True
        else:
            self.bldr.get_screen("employeeform").ids.emp_salary.error = False

        if self.bldr.get_screen("employeeform").ids.emp_name.error == False and self.bldr.get_screen("employeeform").ids.emp_role.error == False and self.bldr.get_screen("employeeform").ids.emp_salary.error == False:
            print("something vaild")
            self.bldr.get_screen("employeeform").ids.form_spinner.active = True
            thread = threading.Thread(
                target=self.add_employee_to_user,
                args=(email, emp_name, emp_salary, emp_role),
                daemon=True  # Optional: thread app close hone par bhi khatam ho jaye
            )
            thread.start()
        else:
            print("Please fill something")

    def add_employee_to_user(self, email, employee_name, salary, role):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate("office-hub.json")
                firebase_admin.initialize_app(cred)

            db = firestore.client()  # ✅ yeh line add karo

            doc_ref = db.collection('users').document(email)

            # Construct field path: employee.<employee_name>
            field_path = f'employee.{employee_name}'

            # Construct employee data
            employee_data = {
                'salary': salary,
                'role': role
            }

            # Update Firestore with nested field
            doc_ref.set({
                field_path: employee_data
            }, merge=True)

            print(f"Employee '{employee_name}' added to {email} successfully.")
            self.bldr.get_screen("employeeform").ids.form_spinner.active = False
            Clock.schedule_once(lambda dt: self.dialog_of_emp(), 0)
            


        except Exception as e:
            print(f"Error adding employee: {e}")


    def dialog_of_emp(self, dt=None):
        self.dialog = MDDialog(
            title="Employee Added Successfully!",
            text="Do you want to add more Employee?",
            buttons=[
                MDFlatButton(
                    text="Yes",
                    on_release=self.do_yes_action
                ),
                MDFlatButton(
                    text="No",
                    on_release=self.do_no_action
                ),
            ],
        )
        self.dialog.open()

    def do_no_action(self, obj):
        self.dialog.dismiss()  # Dialog dismiss hoga
        self.bldr.get_screen("home").manager.current = "home"

    def do_yes_action(self, obj):
        self.dialog.dismiss()  # Dialog dismiss hoga
        # Reset fields in employeeform
        self.bldr.get_screen("employeeform").ids.emp_name.text = ""
        self.bldr.get_screen("employeeform").ids.emp_role.text = ""
        self.bldr.get_screen("employeeform").ids.emp_salary.text = ""
        self.bldr.get_screen("employeeform").manager.current = "employeeform"




    def inward_screen(self):
        self.bldr.get_screen("inward").manager.current = "inward"

    def outward_screen(self):
        self.bldr.get_screen("outward").manager.current = "outward"

    def inward_entry(self):
        date = self.bldr.get_screen("inward").ids.date_field.text
        invoice = self.bldr.get_screen("inward").ids.invoice_field.text
        time = self.bldr.get_screen("inward").ids.time_field.text
        party = self.bldr.get_screen("inward").ids.party_field.text
        article = self.bldr.get_screen("inward").ids.article_field.text
        qty = self.bldr.get_screen("inward").ids.qty_field.text
        amount = self.bldr.get_screen("inward").ids.amount_field.text
        vehicle = self.bldr.get_screen("inward").ids.vehicle_field.text
         # ✅ Read user email
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
        email = user_data.get("email")
        if date != "" and invoice != "" and time != "" and party != "" and article != "" and qty != "" and amount != "" and vehicle != "":

            self.bldr.get_screen("inward").ids.inward_spinner.active = True
            storage_thread = threading.Thread(
                target=self.save_inward_entry,
                args=(date, email, invoice,time, party, article, qty, amount, vehicle),
                daemon=True  # Ensures thread exits when app closes
            )
            storage_thread.start()
        else:
            self.bldr.get_screen("inward").ids.date_field.error = True
            self.bldr.get_screen("inward").ids.invoice_field.error = True
            self.bldr.get_screen("inward").ids.time_field.error = True
            self.bldr.get_screen("inward").ids.party_field.error = True
            self.bldr.get_screen("inward").ids.article_field.error = True
            self.bldr.get_screen("inward").ids.qty_field.error = True
            self.bldr.get_screen("inward").ids.amount_field.error = True
            self.bldr.get_screen("inward").ids.vehicle_field.error = True





    def save_inward_entry(self, date, email, invoice, time, party, article, quantity, amount, vehicle):
        try:
            # ✅ Firebase Init
            if not firebase_admin._apps:
                if os.path.exists("office-hub.json"):
                    cred = credentials.Certificate("office-hub.json")
                    firebase_admin.initialize_app(cred)
                else:
                    print("❌ Firebase credential file not found.")
                    return

            db = firestore.client()


            # ✅ Entry Data
            entry_data = {
                "date": date,
                "invoice": invoice,
                "time": time,
                "party": party,
                "article": article,
                "quantity": quantity,
                "amount": amount,
                "vehicle": vehicle
            }

            # ✅ Save in inward map field
            doc_ref = db.collection("users").document(email)
            doc_ref.set({
                "inward": {
                    invoice: entry_data
                }
            }, merge=True)

            print("✅ Entry saved under 'inward' field!")
            self.bldr.get_screen("inward").ids.inward_spinner.active = False
            Clock.schedule_once(lambda dt: self.dialog_of_entries(), 0)

        except Exception as e:
            print("❌ Error while saving inward entry:", e)

    


    def dialog_of_entries(self, dt=None):
        self.bldr.get_screen("inward").ids.date_field.text = ""
        self.bldr.get_screen("inward").ids.invoice_field.text = ""
        self.bldr.get_screen("inward").ids.time_field.text = ""
        self.bldr.get_screen("inward").ids.party_field.text = ""
        self.bldr.get_screen("inward").ids.article_field.text = ""
        self.bldr.get_screen("inward").ids.qty_field.text = ""
        self.bldr.get_screen("inward").ids.amount_field.text = ""
        self.bldr.get_screen("inward").ids.vehicle_field.text = ""
        self.dialog = MDDialog(
            title="Entry Successfull!",
            text="Entry successfully added to database",
        )
        self.dialog.open()

    def aboutappscreen(self):
        self.bldr.get_screen("aboutapp").manager.current = "aboutapp"

    def aboutdevscreen(self):
        self.bldr.get_screen("aboutdev").manager.current = "aboutdev"

    def themescreen(self):
        self.bldr.get_screen("themes").manager.current = "themes"

    def toggle_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


    def outward_entry(self):
        date = self.bldr.get_screen("outward").ids.date_field_out.text
        invoice = self.bldr.get_screen("outward").ids.invoice_field_out.text
        time = self.bldr.get_screen("outward").ids.time_field_out.text
        party = self.bldr.get_screen("outward").ids.party_field_out.text
        article = self.bldr.get_screen("outward").ids.article_field_out.text
        qty = self.bldr.get_screen("outward").ids.qty_field_out.text
        amount = self.bldr.get_screen("outward").ids.amount_field_out.text
        vehicle = self.bldr.get_screen("outward").ids.vehicle_field_out.text
         # ✅ Read user email
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
        email = user_data.get("email")
        if date != "" and invoice != "" and time != "" and party != "" and article != "" and qty != "" and amount != "" and vehicle != "":

            self.bldr.get_screen("outward").ids.outward_spinner.active = True
            storage_thread = threading.Thread(
                target=self.save_outward_entry,
                args=(date, email, invoice,time, party, article, qty, amount, vehicle),
                daemon=True  # Ensures thread exits when app closes
            )
            storage_thread.start()
        else:
            self.bldr.get_screen("outward").ids.date_field_out.error = True
            self.bldr.get_screen("outward").ids.invoice_field_out.error = True
            self.bldr.get_screen("outward").ids.time_field_out.error = True
            self.bldr.get_screen("outward").ids.party_field_out.error = True
            self.bldr.get_screen("outward").ids.article_field_out.error = True
            self.bldr.get_screen("outward").ids.qty_field_out.error = True
            self.bldr.get_screen("outward").ids.amount_field_out.error = True
            self.bldr.get_screen("outward").ids.vehicle_field_out.error = True


    def save_outward_entry(self, date, email, invoice, time, party, article, quantity, amount, vehicle):
        try:
            # ✅ Firebase Init
            if not firebase_admin._apps:
                if os.path.exists("office-hub.json"):
                    cred = credentials.Certificate("office-hub.json")
                    firebase_admin.initialize_app(cred)
                else:
                    print("❌ Firebase credential file not found.")
                    return

            db = firestore.client()


            # ✅ Entry Data
            entry_data = {
                "date": date,
                "invoice": invoice,
                "time": time,
                "party": party,
                "article": article,
                "quantity": quantity,
                "amount": amount,
                "vehicle": vehicle
            }

            # ✅ Save in inward map field
            doc_ref = db.collection("users").document(email)
            doc_ref.set({
                "outward": {
                    invoice: entry_data
                }
            }, merge=True)

            print("✅ Entry saved under 'outward' field!")
            self.bldr.get_screen("outward").ids.outward_spinner.active = False
            Clock.schedule_once(lambda dt: self.dialog_of_entries_out(), 0)

        except Exception as e:
            print("❌ Error while saving inward entry:", e)


    def dialog_of_entries_out(self, dt=None):
        self.bldr.get_screen("outward").ids.date_field_out.text = ""
        self.bldr.get_screen("outward").ids.invoice_field_out.text = ""
        self.bldr.get_screen("outward").ids.time_field_out.text = ""
        self.bldr.get_screen("outward").ids.party_field_out.text = ""
        self.bldr.get_screen("outward").ids.article_field_out.text = ""
        self.bldr.get_screen("outward").ids.qty_field_out.text = ""
        self.bldr.get_screen("outward").ids.amount_field_out.text = ""
        self.bldr.get_screen("outward").ids.vehicle_field_out.text = ""
        self.dialog = MDDialog(
            title="Entry Successfull!",
            text="Entry successfully added to database",
        )
        self.dialog.open()



    def exit(self):
        sys.exit()


    def log_out(self):
        os.remove("user_data.json")
        self.bldr.get_screen("login").manager.current = "login"

    def arrival_screen(self):
        self.bldr.get_screen("arrival").manager.current = "arrival"


    def departure_screen(self):
        self.bldr.get_screen("departure").manager.current = "departure"



    def toggle_sunday(self, instance, value):
        if value:
            self.bldr.get_screen("fillatt").ids.closed.active = False
        print("Sunday:", "ON" if value else "OFF")

    def toggle_closed(self, instance, value):
        if value:
            self.bldr.get_screen("fillatt").ids.sunday.active = False
        print("Closed:", "ON" if value else "OFF")



    def submit_attendence(self):
        Employee = self.bldr.get_screen("fillatt").ids.user_att.text.strip()
        # print(Employee)
        Date = self.bldr.get_screen("fillatt").ids.emp_date.text.strip()
        Time = self.bldr.get_screen("fillatt").ids.emp_time.text.strip()
        # Sunday = self.bldr.get_screen("fillatt").ids.emp_time.sunday

        if not (self.bldr.get_screen("fillatt").ids.sunday.active or self.bldr.get_screen("fillatt").ids.closed.active):

            
            if Date == "" or len(Date) <= 6:
                self.bldr.get_screen("fillatt").ids.emp_date.error = True
                self.bldr.get_screen("fillatt").ids.emp_date.helper_text = "Please Fill a vaild Date"

            else:
                self.bldr.get_screen("fillatt").ids.emp_date.error = False
                self.bldr.get_screen("fillatt").ids.emp_date.helper_text = ""

            if Time == "" or len(Time) <= 4:
                self.bldr.get_screen("fillatt").ids.emp_time.error = True
                self.bldr.get_screen("fillatt").ids.emp_time.helper_text = "Please Fill a vaild Time"

            else:
                self.bldr.get_screen("fillatt").ids.emp_time.error = False
                self.bldr.get_screen("fillatt").ids.emp_time.helper_text = ""

            if self.bldr.get_screen("fillatt").ids.emp_date.error != True and self.bldr.get_screen("fillatt").ids.emp_time.error != True:
                try:
                    self.bldr.get_screen("fillatt").ids.fillatt_spinner.active = True
                    storage_thread = threading.Thread(
                        target=self.save_attendance_opened,
                        args=(Employee, Date, Time),
                        daemon=True  # Ensures thread exits when app closes
                    )
                    storage_thread.start()

                except Exception as e:
                    print(e)

            else:
                print("Please validate tha data")

        else:
            print("Today is sunday or closed")
            self.bldr.get_screen("fillatt").ids.emp_date.text = ""
            self.bldr.get_screen("fillatt").ids.emp_time.text = ""

            if Date == "" or len(Date) <= 4:
                self.bldr.get_screen("fillatt").ids.emp_date.error = True
                self.bldr.get_screen("fillatt").ids.emp_date.helper_text = "Please Fill a vaild Date"
            else:
                if self.bldr.get_screen("fillatt").ids.sunday.active == True:
                    self.bldr.get_screen("fillatt").ids.fillatt_spinner.active = True
                    storage_thread = threading.Thread(
                        target=self.save_attendance_closed,
                        args=(Employee, Date, "Sunday"),
                        daemon=True  # Ensures thread exits when app closes
                    )
                    storage_thread.start()
                elif self.bldr.get_screen("fillatt").ids.closed.active == True:
                    self.bldr.get_screen("fillatt").ids.fillatt_spinner.active = True
                    storage_thread = threading.Thread(
                        target=self.save_attendance_closed,
                        args=(Employee, Date, "Closed"),
                        daemon=True  # Ensures thread exits when app closes
                    )
                    storage_thread.start()


    
    def save_attendance_closed(self, employee_name, date, arrival_time):
        try:
            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate("office-hub.json")
                firebase_admin.initialize_app(cred)

            db = firestore.client()

            # Load email from user_data.json
            if not os.path.exists("user_data.json"):
                raise FileNotFoundError("user_data.json file not found!")

            with open("user_data.json", "r") as f:
                user_data = json.load(f)
            
            email = user_data.get("email")
            if not email:
                raise ValueError("Email not found in user_data.json")

            # Save attendance data
            db.collection("users").document(email).update({
                f"Attendance.{employee_name}.{date}.arrival": arrival_time
            })

            print("Attendance saved successfully.")
            
            Clock.schedule_once(lambda dt: self.arrival_attendence_dialog(), 0)


        except Exception as e:
            print("Error saving attendance:", e)


    def save_attendance_opened(self, employee_name, date, arrival_time):
        try:
            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate("office-hub.json")
                firebase_admin.initialize_app(cred)

            db = firestore.client()

            # Load email from user_data.json
            if not os.path.exists("user_data.json"):
                raise FileNotFoundError("user_data.json file not found!")

            with open("user_data.json", "r") as f:
                user_data = json.load(f)
            
            email = user_data.get("email")
            if not email:
                raise ValueError("Email not found in user_data.json")

            # Save attendance data
            db.collection("users").document(email).update({
                f"Attendance.{employee_name}.{date}.arrival": arrival_time
            })

            print("Attendance saved successfully.")
            
            Clock.schedule_once(lambda dt: self.arrival_attendence_dialog(), 0)


        except Exception as e:
            print("Error saving attendance:", e)


    def arrival_attendence_dialog(self):
        self.bldr.get_screen("fillatt").ids.fillatt_spinner.active = False
        self.bldr.get_screen("fillatt").ids.emp_date.text = ""
        self.bldr.get_screen("fillatt").ids.emp_time.text = ""
        self.dialog = MDDialog(
            title="Attendence Submitted Successfully Added!",
            text=f"Your Attendence successfully added to database please add departure attendence of the employee at time.",
            size_hint=(0.8, None),
                # buttons=[
                #     MDRaisedButton(
                #         text="OK",
                #         on_release=lambda x: self.dialog.dismiss(),
                #         color = "FF69B4"
                #     ),
                # ],
        )
        self.dialog.open()

    def submit_attendence_dep(self):
        Employee = self.bldr.get_screen("fillattdep").ids.user_att_dep.text.strip()
        # print(Employee)
        Date = self.bldr.get_screen("fillattdep").ids.emp_date_dep.text.strip()
        Time = self.bldr.get_screen("fillattdep").ids.emp_time_dep.text.strip()
        # Sunday = self.bldr.get_screen("fillatt").ids.emp_time.sunday

        if not (self.bldr.get_screen("fillattdep").ids.sunday_dep.active or self.bldr.get_screen("fillattdep").ids.closed_dep.active):

            
            if Date == "" or len(Date) <= 6:
                self.bldr.get_screen("fillattdep").ids.emp_date_dep.error = True
                self.bldr.get_screen("fillattdep").ids.emp_date_dep.helper_text = "Please Fill a vaild Date"

            else:
                self.bldr.get_screen("fillattdep").ids.emp_date_dep.error = False
                self.bldr.get_screen("fillattdep").ids.emp_date_dep.helper_text = ""

            if Time == "" or len(Time) <= 4:
                self.bldr.get_screen("fillattdep").ids.emp_time_dep.error = True
                self.bldr.get_screen("fillattdep").ids.emp_time_dep.helper_text = "Please Fill a vaild Time"

            else:
                self.bldr.get_screen("fillattdep").ids.emp_time_dep.error = False
                self.bldr.get_screen("fillattdep").ids.emp_time_dep.helper_text = ""

            if self.bldr.get_screen("fillattdep").ids.emp_date_dep.error != True and self.bldr.get_screen("fillattdep").ids.emp_time_dep.error != True:
                try:
                    self.bldr.get_screen("fillattdep").ids.fillattdep_spinner.active = True
                    storage_thread = threading.Thread(
                        target=self.save_attendance_opened_dep,
                        args=(Employee, Date, Time),
                        daemon=True  # Ensures thread exits when app closes
                    )
                    storage_thread.start()

                    print(Date)
                    print(Employee)
                    print(Time)

                except Exception as e:
                    print(e)

            else:
                print("Please validate tha data")

        else:
            print("Today is sunday or closed")
            self.bldr.get_screen("fillattdep").ids.emp_date_dep.text = ""
            self.bldr.get_screen("fillattdep").ids.emp_time_dep.text = ""

            if Date == "" or len(Date) <= 4:
                self.bldr.get_screen("fillattdep").ids.emp_date_dep.error = True
                self.bldr.get_screen("fillattdep").ids.emp_date_dep.helper_text = "Please Fill a vaild Date"
            else:
                if self.bldr.get_screen("fillattdep").ids.sunday_dep.active == True:
                    self.bldr.get_screen("fillattdep").ids.fillattdep_spinner.active = True
                    storage_thread = threading.Thread(
                        target=self.save_attendance_closed_dep,
                        args=(Employee, Date, "Sunday"),
                        daemon=True  # Ensures thread exits when app closes
                    )
                    storage_thread.start()
                elif self.bldr.get_screen("fillattdep").ids.closed_dep.active == True:
                    self.bldr.get_screen("fillattdep").ids.fillattdep_spinner.active = True
                    storage_thread = threading.Thread(
                        target=self.save_attendance_closed_dep,
                        args=(Employee, Date, "Closed"),
                        daemon=True  # Ensures thread exits when app closes
                    )
                    storage_thread.start()



    def save_attendance_opened_dep(self, employee_name, date, arrival_time):
        try:
            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate("office-hub.json")
                firebase_admin.initialize_app(cred)

            db = firestore.client()

            # Load email from user_data.json
            if not os.path.exists("user_data.json"):
                raise FileNotFoundError("user_data.json file not found!")

            with open("user_data.json", "r") as f:
                user_data = json.load(f)
            
            email = user_data.get("email")
            if not email:
                raise ValueError("Email not found in user_data.json")

            # Save attendance data
            db.collection("users").document(email).update({
                f"Attendance.{employee_name}.{date}.departure": arrival_time
            })

            print("Attendance saved successfully.")
            
            Clock.schedule_once(lambda dt: self.arrival_attendence_dep_dialog(), 0)


        except Exception as e:
            print("Error saving attendance:", e)


    def save_attendance_closed_dep(self, employee_name, date, arrival_time):
        try:
            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate("office-hub.json")
                firebase_admin.initialize_app(cred)

            db = firestore.client()

            # Load email from user_data.json
            if not os.path.exists("user_data.json"):
                raise FileNotFoundError("user_data.json file not found!")

            with open("user_data.json", "r") as f:
                user_data = json.load(f)
            
            email = user_data.get("email")
            if not email:
                raise ValueError("Email not found in user_data.json")

            # Save attendance data
            db.collection("users").document(email).update({
                f"Attendance.{employee_name}.{date}.departure": arrival_time
            })

            print("Attendance saved successfully.")
            
            Clock.schedule_once(lambda dt: self.arrival_attendence_dep_dialog(), 0)


        except Exception as e:
            print("Error saving attendance:", e)



    def arrival_attendence_dep_dialog(self):
        self.bldr.get_screen("fillattdep").ids.fillattdep_spinner.active = False
        self.bldr.get_screen("fillattdep").ids.emp_date_dep.text = ""
        self.bldr.get_screen("fillattdep").ids.emp_time_dep.text = ""
        self.dialog = MDDialog(
            title="Attendence Submitted Successfully Added!",
            text=f"Your Attendence successfully added to database please add departure attendence of the employee at time.",
            size_hint=(0.8, None),
                # buttons=[
                #     MDRaisedButton(
                #         text="OK",
                #         on_release=lambda x: self.dialog.dismiss(),
                #         color = "FF69B4"
                #     ),
                # ],
        )
        self.dialog.open()














    
if __name__ == "__main__":
    MyApp().run()