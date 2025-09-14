"""
Example usage of FormStepperWidget.
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QLabel, QLineEdit, QTextEdit, QCheckBox, QComboBox,
                             QPushButton, QFormLayout, QHBoxLayout)
from PyQt6.QtCore import Qt

# Add the parent directory to the path to import the widgets
sys.path.append('..')

from forms.form_stepper import FormStepperWidget, SimpleFormStepper


class FormStepperExample(QMainWindow):
    """Example application for FormStepperWidget."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form Stepper Example")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Form stepper
        self.stepper = FormStepperWidget()
        self.stepper.step_changed.connect(self.on_step_changed)
        self.stepper.step_completed.connect(self.on_step_completed)
        self.stepper.form_completed.connect(self.on_form_completed)

        # Add steps
        self.create_steps()

        layout.addWidget(self.stepper)

        # Simple stepper example
        layout.addWidget(QLabel("Simple Stepper:"))

        step_titles = ["Personal Info", "Contact Details", "Preferences", "Review"]
        self.simple_stepper = SimpleFormStepper(step_titles)
        self.simple_stepper.step_changed.connect(self.on_simple_step_changed)
        layout.addWidget(self.simple_stepper)

    def create_steps(self):
        """Create form steps."""
        # Step 1: Personal Information
        step1_widget = QWidget()
        step1_layout = QFormLayout(step1_widget)

        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.email = QLineEdit()

        step1_layout.addRow("First Name:", self.first_name)
        step1_layout.addRow("Last Name:", self.last_name)
        step1_layout.addRow("Email:", self.email)

        self.stepper.add_step(
            "Personal Information",
            step1_widget,
            "Enter your basic personal details",
            self.validate_step1
        )

        # Step 2: Contact Details
        step2_widget = QWidget()
        step2_layout = QFormLayout(step2_widget)

        self.phone = QLineEdit()
        self.address = QTextEdit()
        self.address.setMaximumHeight(100)
        self.country = QComboBox()
        self.country.addItems(["USA", "Canada", "UK", "Australia", "Germany"])

        step2_layout.addRow("Phone:", self.phone)
        step2_layout.addRow("Address:", self.address)
        step2_layout.addRow("Country:", self.country)

        self.stepper.add_step(
            "Contact Details",
            step2_widget,
            "Provide your contact information",
            self.validate_step2
        )

        # Step 3: Preferences
        step3_widget = QWidget()
        step3_layout = QVBoxLayout(step3_widget)

        step3_layout.addWidget(QLabel("Select your preferences:"))

        self.newsletter = QCheckBox("Subscribe to newsletter")
        self.notifications = QCheckBox("Enable notifications")
        self.marketing = QCheckBox("Receive marketing emails")

        step3_layout.addWidget(self.newsletter)
        step3_layout.addWidget(self.notifications)
        step3_layout.addWidget(self.marketing)
        step3_layout.addStretch()

        self.stepper.add_step(
            "Preferences",
            step3_widget,
            "Configure your account preferences"
        )

        # Step 4: Review
        step4_widget = QWidget()
        step4_layout = QVBoxLayout(step4_widget)

        step4_layout.addWidget(QLabel("Review your information:"))

        self.review_label = QLabel("Complete previous steps to see review")
        self.review_label.setWordWrap(True)
        step4_layout.addWidget(self.review_label)
        step4_layout.addStretch()

        self.stepper.add_step(
            "Review & Submit",
            step4_widget,
            "Review your information before submitting"
        )

    def validate_step1(self) -> bool:
        """Validate step 1."""
        if not self.first_name.text().strip():
            print("First name is required")
            return False
        if not self.last_name.text().strip():
            print("Last name is required")
            return False
        if not self.email.text().strip() or "@" not in self.email.text():
            print("Valid email is required")
            return False
        return True

    def validate_step2(self) -> bool:
        """Validate step 2."""
        if not self.phone.text().strip():
            print("Phone number is required")
            return False
        if not self.address.toPlainText().strip():
            print("Address is required")
            return False
        return True

    def on_step_changed(self, step_index):
        """Handle step change."""
        print(f"Step changed to: {step_index}")

        # Update review when reaching final step
        if step_index == 3:  # Review step
            self.update_review()

    def on_step_completed(self, step_index):
        """Handle step completion."""
        print(f"Step {step_index} completed")

        # Store step data
        if step_index == 0:
            self.stepper.set_step_data(step_index, {
                'first_name': self.first_name.text(),
                'last_name': self.last_name.text(),
                'email': self.email.text()
            })
        elif step_index == 1:
            self.stepper.set_step_data(step_index, {
                'phone': self.phone.text(),
                'address': self.address.toPlainText(),
                'country': self.country.currentText()
            })
        elif step_index == 2:
            self.stepper.set_step_data(step_index, {
                'newsletter': self.newsletter.isChecked(),
                'notifications': self.notifications.isChecked(),
                'marketing': self.marketing.isChecked()
            })

    def on_form_completed(self, all_data):
        """Handle form completion."""
        print("Form completed!")
        print("All data:", all_data)

    def update_review(self):
        """Update review information."""
        review_text = "Review Information:\n\n"

        # Personal info
        step0_data = self.stepper.get_step_data(0)
        if step0_data:
            review_text += "Personal Information:\n"
            review_text += f"Name: {step0_data.get('first_name', '')} {step0_data.get('last_name', '')}\n"
            review_text += f"Email: {step0_data.get('email', '')}\n\n"

        # Contact info
        step1_data = self.stepper.get_step_data(1)
        if step1_data:
            review_text += "Contact Details:\n"
            review_text += f"Phone: {step1_data.get('phone', '')}\n"
            review_text += f"Country: {step1_data.get('country', '')}\n"
            review_text += f"Address: {step1_data.get('address', '')}\n\n"

        # Preferences
        step2_data = self.stepper.get_step_data(2)
        if step2_data:
            review_text += "Preferences:\n"
            review_text += f"Newsletter: {'Yes' if step2_data.get('newsletter') else 'No'}\n"
            review_text += f"Notifications: {'Yes' if step2_data.get('notifications') else 'No'}\n"
            review_text += f"Marketing: {'Yes' if step2_data.get('marketing') else 'No'}\n"

        self.review_label.setText(review_text)

    def on_simple_step_changed(self, step_index):
        """Handle simple stepper step change."""
        print(f"Simple stepper step: {step_index}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = FormStepperExample()
    window.show()

    sys.exit(app.exec())