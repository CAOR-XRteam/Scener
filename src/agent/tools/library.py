from langchain_core.tools import tool
from library import api
from loguru import logger
from colorama import Fore


@tool
def list_assets() -> str:
    """Retrieve the list of assets with their element paths in the database."""
    logger.info(f"Using tool {Fore.GREEN}{'list_asset'}{Fore.RESET}")
    return api.list_asset()

@tool
def update_asset(name: str, image_path: str, mesh_path: str, description_path: str) -> str:
    """Update an existing asset by name with image path, mesh path, and description path."""
    logger.info(f"Using tool {Fore.GREEN}{'update_asset'}{Fore.RESET}")
    api.update_asset(name, image_path, mesh_path, description_path)
    return "asset updated"

@tool
def create_description_file(path_with_name: str, asset_description: str) -> str:
    """Create a text file with the given content. The name of the file should be the same than the asset name"""
    logger.info(f"Using tool {Fore.GREEN}{'create_description_file'}{Fore.RESET}")
    try:
        with open(path_with_name, 'w') as file:
            file.write(asset_description)
        return f"Text file '{path_with_name}' created successfully."
    except Exception as e:
        return f"Failed to create text file: {str(e)}"
