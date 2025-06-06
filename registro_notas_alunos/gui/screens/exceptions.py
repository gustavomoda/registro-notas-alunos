"""
Exceções específicas para as telas da interface gráfica (GUI).

Este módulo centraliza todas as exceções customizadas utilizadas
nas telas do sistema, seguindo o princípio DRY e facilitando
a manutenção e reutilização.
"""


class GUIBaseException(Exception):
    """Exceção base para todas as exceções da GUI"""

    pass


class ValidationError(GUIBaseException):
    """Erro de validação de dados de entrada"""

    pass


class DataNotFoundError(GUIBaseException):
    """Erro quando dados esperados não são encontrados"""

    pass


class SelectionError(GUIBaseException):
    """Erro relacionado à seleção de itens na interface"""

    pass


class DatabaseConnectionError(GUIBaseException):
    """Erro de conexão com banco de dados"""

    pass


class FormError(GUIBaseException):
    """Erro relacionado ao preenchimento de formulários"""

    pass


class NavigationError(GUIBaseException):
    """Erro relacionado à navegação entre telas"""

    pass


class PermissionError(GUIBaseException):
    """Erro relacionado a permissões de acesso"""

    pass


# Aliases para manter compatibilidade e facilitar imports
__all__ = [
    "GUIBaseException",
    "ValidationError",
    "DataNotFoundError",
    "SelectionError",
    "DatabaseConnectionError",
    "FormError",
    "NavigationError",
    "PermissionError",
]
