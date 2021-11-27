import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import glob
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# image directory
mypath = 'test_data/images/'

# create sorted image names list
glob_name = "test_data\\images\\*.jpg"
sorted_image_names = glob.glob(glob_name)


# used to help create labels
def string_between_two_commas(string, start_comma_number, end_comma_number):
    # find index of first nth comma
    parts1 = string.split(",", start_comma_number)
    start_index = len(string) - len(parts1[-1])

    # find index of second nth comma
    parts2 = string.split(",", end_comma_number)
    end_index = len(string) - len(parts2[-1]) - 1

    # return string between two commas
    return string[start_index: end_index]


labels = []

# create labels for nvidia dataset
with open('data/data.csv') as file:
    train_file = file.readlines()
    for index, line in enumerate(train_file):
        # skips first line and only appends center images
        if index != 0 and string_between_two_commas(line, 4, 5)[0] == "c":
            x = string_between_two_commas(line, 6, 7)
            labels.append(float(x))

labels = labels[0:3000]

# data directory
data_dir = 'test_data/'

# create dataset
testing_dataset = image_dataset_from_directory(data_dir, labels=labels, batch_size=1, image_size=(455, 256),
                                               shuffle=False, seed=None, validation_split=None, subset=None)

# load saved model
model = tf.keras.models.load_model('model')

image_sort_by_acc = []

# run dataset
for step, (x_batch_train, y_batch_train) in enumerate(testing_dataset):
    pred_tensor = model(x_batch_train, training=None)
    pred_float = pred_tensor.numpy().astype(float)
    expected_float = y_batch_train.numpy().astype(float)
    print("Predicted Value: ", pred_float[0][0], "   |||   ", "Actual Value: ",
          expected_float[0], "   |||   ", "Difference: ", abs(pred_float[0][0] - expected_float[0]))
    image_sort_by_acc.append((abs(pred_float[0][0] - expected_float[0]), sorted_image_names[step]))

image_sort_by_acc.sort()

# initialize tkinter variables
top_check = False
bottom_check = False
num_of_images = 0


# define tkinter checkbox functions
def change_top_check():
    global top_check
    if top_check is False:
        top_check = True
    else:
        top_check = False


def change_bottom_check():
    global bottom_check
    if bottom_check is False:
        bottom_check = True
    else:
        bottom_check = False


# define tkinter button on-click function
def click():
    global user_entry
    global num_of_images
    num_of_images = int(user_entry.get())
    add_images()


# attach scrollbar to both tkinter text windows
def multiple_yview(*args):
    st1.yview(*args)
    st2.yview(*args)


# needed for tkinter to hold display pictures in memory
pics1 = []
pics2 = []


def add_images():
    # clear old text
    st1.delete('1.0', END)
    st2.delete('1.0', END)

    for j in range(num_of_images):
        if top_check is True and bottom_check is True:
            # Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object
            pics1.append(ImageTk.PhotoImage(Image.open(image_sort_by_acc[-1 - j][1])))
            pics2.append(ImageTk.PhotoImage(Image.open(image_sort_by_acc[j][1])))

            # add images to text fields
            st1.image_create(END, image=pics1[j])
            st2.image_create(END, image=pics2[j])

            # add data to text fields
            st1.insert(END, '\n')
            st1.insert(str(j*3+2) + ".0", "Picture name: " + str(image_sort_by_acc[-1 - j][1]))
            st1.insert(END, '\n')
            st1.insert(str(j*3+3) + ".0", "Difference: " + str(image_sort_by_acc[-1 - j][0]))
            st1.insert(END, '\n')

            st2.insert(END, '\n')
            st2.insert(str(j*3+2) + ".0", "Picture name: " + str(image_sort_by_acc[j][1]))
            st2.insert(END, '\n')
            st2.insert(str(j*3+3) + ".0", "Difference: " + str(image_sort_by_acc[j][0]))
            st2.insert(END, '\n')

        elif top_check is True and bottom_check is False:
            # Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object
            pics2.append(ImageTk.PhotoImage(Image.open(image_sort_by_acc[j][1])))

            # add images to text fields
            st2.image_create(END, image=pics2[j])

            # add data to text fields
            st2.insert(END, '\n')
            st2.insert(str(j * 3 + 2) + ".0", "Picture name: " + str(image_sort_by_acc[j][1]))
            st2.insert(END, '\n')
            st2.insert(str(j * 3 + 3) + ".0", "Difference: " + str(image_sort_by_acc[j][0]))
            st2.insert(END, '\n')

        else:
            # Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object
            pics1.append(ImageTk.PhotoImage(Image.open(image_sort_by_acc[-1 - j][1])))

            # add images to text fields
            st1.image_create(END, image=pics1[j])

            # add data to text fields
            st1.insert(END, '\n')
            st1.insert(str(j * 3 + 2) + ".0", "Picture name: " + str(image_sort_by_acc[-1 - j][1]))
            st1.insert(END, '\n')
            st1.insert(str(j * 3 + 3) + ".0", "Difference: " + str(image_sort_by_acc[-1 - j][0]))
            st1.insert(END, '\n')


# create tkinter window and define size
window = Tk()
window.geometry("1500x900")
window.title("Image Viewer")

window_frame = Frame(window)
window_frame.pack(pady=20)

# Initialize a tkinter label
label = Label(window_frame, text="Number of images to show:", font=("Helvetica"))
label.pack()

# Create a tkinter entry widget to accept user input
user_entry = Entry(window_frame, width=40)
user_entry.pack()

# tkinter variables used to check state of boxes
var_top = IntVar()
var_bottom = IntVar()

# tkinter checkboxes
check_bottom = Checkbutton(window_frame, command=change_bottom_check,
                           text="Show images with lowest accuracy (left side)", variable=var_bottom, onvalue=1,
                           offvalue=0)
check_bottom.pack()

check_top = Checkbutton(window_frame, command=change_top_check, text="Show images with highest accuracy (right side)",
                        variable=var_top, onvalue=1, offvalue=0)
check_top.pack()

# Create a tkinter button to show images
ttk.Button(window_frame, text="Display Images", width=20, command=click).pack(pady=20)

# create a tkinter scrollbar
text_scroll = Scrollbar(window_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# create two tkinter text fields, positioned side by side
st1 = Text(window_frame, width=80, height=50, yscrollcommand=text_scroll.set)
st1.pack(side=LEFT, padx=5)
st2 = Text(window_frame, width=80, height=50, yscrollcommand=text_scroll.set)
st2.pack(side=RIGHT)

# configure tkinter scrollbar
text_scroll.config(command=multiple_yview)

# open tkinter window
window.mainloop()
