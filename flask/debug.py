from colorama import Fore, Back, Style
"""
視覺化輸出debug工具
by.rex
2023/8/31
"""
class debug:
    """
    Color Output
    """

    __yellow = Fore.YELLOW
    __blue = Fore.BLUE
    __white = Fore.WHITE

    __bg_yellow = Back.YELLOW
    __bg_blue = Back.BLUE

    __remove = Style.RESET_ALL

    @staticmethod
    def yellow(*args):
        """
        make text yellow
        """
        for arg in args:
            print(debug.__yellow+arg+debug.__remove)

    @staticmethod
    def blue(*args):
        """
        make text blue
        """
        for arg in args:
            print(debug.__blue+arg+debug.__remove)


    @staticmethod
    def bg_yellow(*args):
        """
        make background yellow
        """
        for arg in args:
            print(debug.__bg_yellow+debug.__white+arg+debug.__remove)
    @staticmethod
    def bg_blue(*args):
        """
        make background blue
        """
        for arg in args:
            print(debug.__bg_blue+arg+debug.__remove)
    
    @staticmethod
    def panel(title,*args, **kwargs):
        """
        ************\n
        panel title
        
        something
        some key : some value

        ************
        """
        debug.blue("\n****************************\n")
        debug.yellow(title+"\n")
        if args:
            for arg in args:
                print(arg)
        if kwargs:
            for key, value in kwargs.items():
                print(debug.__yellow+key+":"+debug.__remove,value)
        debug.blue("\n****************************\n")

    @staticmethod
    def hr():
        debug.blue("\n****************************\n")