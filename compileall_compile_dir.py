import compileall
import glob


# def show(title):
#     print(title)
#     for filename in glob.glob('obd/**',recursive=True):
#         print('  {}'.format(filename))
#     print()


# show('Before')
compileall.compile_dir('/Users/cristianku/Documents/PycharmProjects/car-computer-raspberry/obd', force=True)

# show('\nAfter')