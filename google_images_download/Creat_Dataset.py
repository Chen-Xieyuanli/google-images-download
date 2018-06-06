#Creating dataset for Bonnet

import google_images_download   #importing the library

#------------- Main Program -------------#
# def main():
#     records = user_input()
#     for arguments in records:
#
#         if arguments['single_image']:  # Download Single Image using a URL
#             response = googleimagesdownload()
#             response.single_image(arguments['single_image'])
#         else:  # or download multiple images based on keywords/keyphrase search
#             t0 = time.time()  # start the timer
#             response = googleimagesdownload()
#             paths = response.download(arguments)  #wrapping response in a variable just for consistency
#
#             print("\nEverything downloaded!")
#             t1 = time.time()  # stop the timer
#             total_time = t1 - t0  # Calculating the total time required to crawl, find and download all the links of 60,000 images
#             print("Total time taken: " + str(total_time) + " Seconds")
#
# if __name__ == "__main__":
#     main()

response = google_images_download.googleimagesdownload()   #class instantiation
arguments = {"keywords":"Polar bears","limit":20,"proxy":"127.0.0.1:8123"}   #creating list of arguments
paths = response.download(arguments)   #passing the arguments to the function
print(paths)   #printing absolute paths of the downloaded images