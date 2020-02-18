import os


def create_docker_file():
    os.system("rm -rf Dockerfile")
    file_instance = open("Dockerfile", "w+")
    base_image = "FROM nginx:alpine"
    path_to_files = "COPY index.html /usr/share/nginx/html/index.html"
    file_instance.write(base_image)
    file_instance.write("\n")
    file_instance.write("RUN  rm -rf /usr/share/nginx/html/**.html")
    file_instance.write("\n")
    file_instance.write(path_to_files)
    file_instance.write("\n")
    file_instance.write("EXPOSE 80")
