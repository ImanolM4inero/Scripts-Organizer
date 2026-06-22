import os
import shutil
from pathlib import Path
from datetime import datetime
import logging

DOWNLOADS_FOLDER = Path(r"C:\home\Downloads")
LOG_FILE = DOWNLOADS_FOLDER / "organizador_log.txt"

EXTENSIONS = {
    'imagenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
    'iso': ['.iso', '.img'],
    'logs': ['.log', '.txt'],
    'exe': ['.exe'],
    'msi': ['.msi'],
    'pdf': ['.pdf'],
    'office': ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp']
}

DESTINATION_FOLDERS = {
    'imagenes', 'archivos', 'programas', 'documentos'
}

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def create_folder_structure(base_path):
    """Crea la estructura de carpetas necesaria"""
    folders = {
        'imagenes': [],
        'archivos': ['iso_logs', 'otros'],
        'programas': ['exe', 'msi'],
        'documentos': ['pdf', 'office']
    }
    
    for main_folder, subfolders in folders.items():
        main_path = base_path / main_folder
        main_path.mkdir(exist_ok=True)
        
        for subfolder in subfolders:
            sub_path = main_path / subfolder
            sub_path.mkdir(exist_ok=True)

def get_destination_file(file_extension, base_path):
    """Determina la carpeta de destino según la extensión del archivo"""
    ext = file_extension.lower()
    
    if ext in EXTENSIONS['imagenes']:
        return base_path / 'imagenes'
    elif ext in EXTENSIONS['iso']:
        return base_path / 'archivos' / 'iso_logs'
    elif ext in EXTENSIONS['logs']:
        return base_path / 'archivos' / 'iso_logs'
    elif ext in EXTENSIONS['exe']:
        return base_path / 'programas' / 'exe'
    elif ext in EXTENSIONS['msi']:
        return base_path / 'programas' / 'msi'
    elif ext in EXTENSIONS['pdf']:
        return base_path / 'documentos' / 'pdf'
    elif ext in EXTENSIONS['office']:
        return base_path / 'documentos' / 'office'
    else:
        return base_path / 'archivos' / 'otros'

def should_skip_file(file_path, base_path):
    """Determina si un archivo debe ser ignorado"""
  
    if file_path.is_dir():
        return True
    
    if file_path.name.startswith('.') or file_path.name.endswith('.tmp'):
        return True
    
    try:
        relative_path = file_path.relative_to(base_path)
        if relative_path.parts[0] in DESTINATION_FOLDERS:
            return True
    except ValueError:
        pass
    
    if file_path.name == __file__:
        return True
    
    return False

def organize_downloads(dry_run=False):
    """Función principal que organiza los archivos"""
    downloads_path = DOWNLOADS_FOLDER
    
    if not downloads_path.exists():
        logging.error(f"La carpeta {DOWNLOADS_FOLDER} no existe.")
        return
    
    logging.info("=" * 60)
    logging.info(f"📂 INICIO DE EJECUCIÓN - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logging.info(f"📁 Carpeta objetivo: {downloads_path}")
    
    if dry_run:
        logging.info("⚠️  MODO PRUEBA (DRY RUN) - Ningún archivo será movido")
    
    create_folder_structure(downloads_path)
    logging.info("✅ Estructura de carpetas verificada")
    
    stats = {
        'total_files': 0,
        'moved_files': 0,
        'skipped_files': 0,
        'errors': 0,
        'by_category': {}
    }
    
    for item in downloads_path.iterdir():
        if should_skip_file(item, downloads_path):
            stats['skipped_files'] += 1
            continue
        
        stats['total_files'] += 1
        
        try:
            destination = get_destination_file(item.suffix, downloads_path)
            
            if dry_run:
                logging.info(f"  📋 [PRUEBA] {item.name} → {destination}")
                stats['moved_files'] += 1
                continue
            
            if (destination / item.name).exists():
                base_name = item.stem
                counter = 1
                new_name = f"{base_name}_{counter}{item.suffix}"
                while (destination / new_name).exists():
                    counter += 1
                    new_name = f"{base_name}_{counter}{item.suffix}"
                shutil.move(str(item), str(destination / new_name))
                logging.info(f"  ✓ {item.name} → {destination} (renombrado a {new_name})")
            else:
                shutil.move(str(item), str(destination / item.name))
                logging.info(f"  ✓ {item.name} → {destination}")
            
            stats['moved_files'] += 1
            
            category = destination.parent.name
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
            
        except Exception as e:
            stats['errors'] += 1
            logging.error(f"  ✗ Error moviendo {item.name}: {str(e)}")
    
    logging.info("")
    logging.info("=" * 60)
    logging.info("📊 RESUMEN DE LA OPERACIÓN")
    logging.info("=" * 60)
    logging.info(f"Total de archivos procesados: {stats['total_files']}")
    logging.info(f"Archivos movidos: {stats['moved_files']}")
    logging.info(f"Archivos omitidos: {stats['skipped_files']}")
    logging.info(f"Errores: {stats['errors']}")
    
    if stats['by_category']:
        logging.info("")
        logging.info("Desglose por categoría:")
        for category, count in stats['by_category'].items():
            logging.info(f"  • {category}: {count} archivos")
    
    logging.info(f"🏁 FINALIZADO - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logging.info("=" * 60)

if __name__ == "__main__":
    print("🔧 Script Organizador de Descargas - Uso Diario")
    print(f"   Ubicación: {DOWNLOADS_FOLDER}")
    print()
    print("Opciones:")
    print("  1. Ejecutar normalmente (mover archivos)")
    print("  2. Modo prueba (solo mostrar qué se movería)")
    print("  3. Salir")
    print()
    
    choice = input("Selecciona una opción (1/2/3): ").strip()
    
    if choice == '1':
        confirm = input("\n¿Deseas continuar? (s/n): ").lower()
        if confirm == 's':
            organize_downloads(dry_run=False)
        else:
            print("❌ Operación cancelada.")
    elif choice == '2':
        print("\n⚠️  Modo prueba activado - Ningún archivo será movido")
        organize_downloads(dry_run=True)
    else:
        print("❌ Operación cancelada.")
