from conans import ConanFile, CMake, tools
import os, sys


class FlatBuffersConan(ConanFile):
    name = "FlatBuffers"
    version = "1.7.1"
    license = "Apache license, v2"
    url = "https://github.com/kenfred/conan-flatbuffers"
    description = """FlatBuffers is an efficient cross platform serialization
                    library for C++, C#, C, Go, Java, JavaScript, PHP, and Python. 
                    It was originally created at Google for game development and 
                    other performance-critical applications."""
    settings = "os", "compiler", "build_type", "arch"
    options = {"code_coverage": [True, False],     # Enable the code coverage build option.
                "build_tests": [True, False],       # Enable the build of tests and samples.
                "build_flatc": [True, False],       # Enable the build of the flatbuffers compiler
                "build_flat_hash": [True, False],   # Enable the build of flathash
                "build_grpc_test": [True, False],   # Enable the build of grpctest
                "shared": [True, False],            # Enable the build of the flatbuffers shared library
            }

    default_options = "code_coverage=False", "build_tests=True", \
                        "build_flatc=True", "build_flat_hash=True", \
                        "build_grpc_test=False", "shared=False"

    output_folder = "flatbuffers"
    

    def config_options(self):
        # NOTE: Code coverage only works on Linux & OSX.
        if self.settings.os == "Windows":
            self.options.remove('code_coverage')

        if self.options.build_tests and not self.options.build_flatc:
            # Must build the compiler to build tests
            self.options.build_tests = False

    def source(self):
        zip_name = "v%s.zip" % self.version if sys.platform == "win32" else "v%s.tar.gz" % self.version
        url = "https://github.com/google/flatbuffers/archive/%s" % (zip_name)
        self.output.info("Downloading %s..." % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self)

        defs = dict()
        if self.settings.os != "Windows":
            defs['FLATBUFFERS_CODE_COVERAGE'] = self.options.code_coverage
        defs['FLATBUFFERS_BUILD_TESTS'] = self.options.build_tests
        defs['FLATBUFFERS_INSTALL'] = True
        defs['FLATBUFFERS_BUILD_FLATLIB'] = not self.options.shared
        defs['FLATBUFFERS_BUILD_SHAREDLIB'] = self.options.shared
        defs['FLATBUFFERS_BUILD_FLATC'] = self.options.build_flatc
        defs['FLATBUFFERS_BUILD_FLATHASH'] = self.options.build_flat_hash
        defs['FLATBUFFERS_BUILD_GRPCTEST'] = self.options.build_grpc_test
        defs['CMAKE_INSTALL_PREFIX'] = self.package_folder

        cmake.configure(source_dir="../flatbuffers-%s" % self.version, build_dir=self.output_folder, defs=defs)
        cmake.build()
        cmake.install()

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["flatbuffers"]
