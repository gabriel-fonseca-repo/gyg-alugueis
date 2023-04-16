from src.extensions import login_manager, security

@login_manager.user_loader
def carregar_usuario(id_usuario):
    return security.datastore.find_user(fs_uniquifier=id_usuario)


