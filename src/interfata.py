import tkinter as tk

from registration_validator import RegistrationValidator


class RegistrationApp:
    def __init__(self, root):
        self.validator = RegistrationValidator(
            existing_usernames={"admin", "Mario"}
        )

        self.root = root
        self.root.title("Registration Validator")

        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self.update_password_feedback)

        tk.Label(root, text="Username:").grid(
            row=0, column=0, sticky="w", padx=10, pady=5
        )
        self.username_entry = tk.Entry(root, width=35)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Email:").grid(
            row=1, column=0, sticky="w", padx=10, pady=5
        )
        self.email_entry = tk.Entry(root, width=35)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Parola:").grid(
            row=2, column=0, sticky="w", padx=10, pady=5
        )
        self.password_entry = tk.Entry(
            root,
            width=35,
            textvariable=self.password_var,
        )
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.strength_label = tk.Label(root, text="Putere: -")
        self.strength_label.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        self.password_errors_label = tk.Label(
            root,
            text="",
            justify="left",
            fg="red",
        )
        self.password_errors_label.grid(
            row=4, column=1, sticky="w", padx=10, pady=5
        )

        tk.Label(root, text="Varsta:").grid(
            row=5, column=0, sticky="w", padx=10, pady=5
        )
        self.age_entry = tk.Entry(root, width=35)
        self.age_entry.grid(row=5, column=1, padx=10, pady=5)

        self.terms_var = tk.BooleanVar()
        self.terms_checkbox = tk.Checkbutton(
            root,
            text="Accept termenii si conditiile ",
            variable=self.terms_var,
        )
        self.terms_checkbox.grid(row=6, column=1, sticky="w", padx=10, pady=5)

        self.submit_button = tk.Button(
            root,
            text="Valideaza inregistrarea",
            command=self.validate_registration,
        )
        self.submit_button.grid(row=7, column=1, sticky="w", padx=10, pady=10)

        self.result_label = tk.Label(
            root,
            text="",
            justify="left",
        )
        self.result_label.grid(
            row=8, column=0, columnspan=2, sticky="w", padx=10, pady=10
        )

    def update_password_feedback(self, *args):
        password = self.password_var.get()

        if password == "":
            self.strength_label.config(text="Putere: -", fg="black")
            self.password_errors_label.config(text="")
            return

        strength = self.validator.password_strength_label(password)
        score = self.validator.password_strength_score(password)

        if strength == "slaba":
            self.strength_label.config(text=f"Putere: slaba ({score}/5)", fg="red")
        elif strength == "medie":
            self.strength_label.config(
                text=f"Putere: medie ({score}/5)", fg="orange"
            )
        else:
            self.strength_label.config(
                text=f"Putere: puternica ({score}/5)", fg="green"
            )

        errors = self.validator.get_password_errors(password)

        if errors:
            self.password_errors_label.config(
                text="\n".join(f"- {error}" for error in errors),
                fg="red",
            )
        else:
            self.password_errors_label.config(
                text="Parola e valida",
                fg="green",
            )

    def validate_registration(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            age = int(self.age_entry.get())
        except ValueError:
            age = None

        accepted_terms = self.terms_var.get()

        errors = self.validator.get_registration_errors(
            username=username,
            email=email,
            password=password,
            age=age,
            accepted_terms=accepted_terms,
        )

        if not errors:
            self.result_label.config(
                text="Datele de inregistrare sunt valide.",
                fg="green",
            )
            return

        result_text = "Datele de inregistrare sunt invalide:\n"

        for field, field_errors in errors.items():
            result_text += f"\n{field}:\n"
            for error in field_errors:
                result_text += f"- {error}\n"

        self.result_label.config(
            text=result_text,
            fg="red",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()