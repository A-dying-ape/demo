from workspace.module import Module
from workspace.mfcase import Mfcase
import multiprocessing


def module_work():
    md = Module()
    md.run()


def mfcase_work():
    mc = Mfcase()
    mc.run()


if __name__ == '__main__':
    t1 = multiprocessing.Process(target=module_work)
    t2 = multiprocessing.Process(target=mfcase_work)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

