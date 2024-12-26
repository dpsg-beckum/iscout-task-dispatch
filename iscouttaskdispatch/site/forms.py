from flask_wtf import FlaskForm
from werkzeug.datastructures.structures import ImmutableMultiDict
from wtforms.fields import (IntegerField, SelectField, StringField,
                            SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Optional


class ITD_Form(FlaskForm):
    # New method to update form values and reprocess the data
    def update_form(self):
        """
        Updates the form's field values and reprocesses the form to ensure the new values are used in rendering.
        This is useful when field values are updated after initial form processing.
        """
        # self.process()
        # Re-process each field with the updated data
        for field in self:
            data = field.data if field.data is not None else ""
            # ensures it re-processes using the current `data`
            field.process(formdata=ImmutableMultiDict(
                {field.name: data}))
            pass

    def get_errors(self) -> list[str]:
        """
        Returns a list of errors in the form.

        Returns:
            list: A list of errors in the form.
        """
        return [_error for _errors in self.errors.values() for _error in _errors]


class ShowTaskForm(ITD_Form):
    comment = TextAreaField("Comment", validators=[Optional()])
    failed = SubmitField("Failed")
    success = SubmitField("Success")


class NewTaskForm(ITD_Form):
    taskID = IntegerField("Task ID", validators=[DataRequired()])
    name = StringField("Name", validators=[Optional()])
    description = TextAreaField("Description", validators=[Optional()])
    format = StringField("Format", validators=[Optional()])
    link = StringField("Link", validators=[Optional()])
    comment = TextAreaField("Comment", validators=[Optional()])
    submit = SubmitField("Create Task")


class EditTaskForm(ITD_Form):
    name = StringField("Name", validators=[Optional()])
    description = TextAreaField("Description", validators=[Optional()])
    format = StringField("Format", validators=[Optional()])
    link = StringField("Link", validators=[Optional()])
    comment = TextAreaField("Comment", validators=[Optional()])
    status = SelectField("Status", validators=[DataRequired()])
    team = SelectField("Team", validators=[DataRequired()])
    delete = SubmitField("Delete Task", name="delete")
    submit = SubmitField("Update Task")


class NewTeamForm(ITD_Form):
    name = StringField("Name", validators=[Optional()])
    submit = SubmitField("Create Team")
