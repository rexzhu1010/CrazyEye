# rex.zhu



import sys,os


if __name__=="__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrazyEye.settings")
    import django
    django.setup()
    #有以上三行，才能调用django数据库

    from  backend import main
    interactive_obj=main.ArgvHandler(sys.argv)
    interactive_obj.call()



