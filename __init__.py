"""
App package initialization
"""

from .dashboard import DashboardApp
from .data_loader import DataManager
from .visualizations import ChartFactory
from .analytics import DataAnalyzer, DataProcessor
from .config import DashboardConfig, UIComponents, SidebarManager
from .pages import (
    OverviewPage,
    WaterSanitationPage,
    EnvironmentPage,
    CrimesPage,
    InfrastructurePage,
    EmploymentPage,
    DataExplorerPage
)

__all__ = [
    'DashboardApp',
    'DataManager',
    'ChartFactory',
    'DataAnalyzer',
    'DataProcessor',
    'DashboardConfig',
    'UIComponents',
    'SidebarManager',
    'OverviewPage',
    'WaterSanitationPage',
    'EnvironmentPage',
    'CrimesPage',
    'InfrastructurePage',
    'EmploymentPage',
    'DataExplorerPage'
]
