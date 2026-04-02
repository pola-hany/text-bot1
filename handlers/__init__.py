from .start_handler import register_start_handlers
from .decoration_handler import register_decoration_handlers
from .translation_handler import register_translation_handlers
from .bios_handler import register_bios_handlers
from .effects_handler import register_effects_handlers
from .callback_handler import register_callback_handlers
from admin.admin_handler import register_admin_handlers

def register_all_handlers(bot):
    register_start_handlers(bot)
    register_decoration_handlers(bot)
    register_translation_handlers(bot)
    register_bios_handlers(bot)
    register_effects_handlers(bot)
    register_callback_handlers(bot)
    register_admin_handlers(bot)

__all__ = ['register_all_handlers']