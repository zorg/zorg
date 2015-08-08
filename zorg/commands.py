class CommandsMixin(object):

    def __init__(self, *args, **kwargs):
        self.commands = {}

        super(CommandsMixin, self).__init__(*args, **kwargs)

    def register_command(self, command_name, command_source):
        self.commands[command_name] = command_source

    def run_command(self, command_name, command_arguments=None):
        if not command_arguments:
            command_arguments = []

        command = self.commands[command_name]

        return command(*command_arguments)

    def serialize(self):
        serialized = super(CommandsMixin, self).serialize()

        serialized["commands"] = self.serialize_commands()

        return serialized

    def serialize_commands(self):
        return self.commands.keys()
