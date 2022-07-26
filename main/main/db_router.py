class DbRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'label':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'label':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == 'label':
            return db == 'default'
        return None
