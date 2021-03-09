from setuptools import setup

package_name = 'irradroom_python'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='romandvorak@mlab.cz',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'distance_measurement = irradroom_python.distance_measurement:main',
            'i2c_devices = irradroom_python.i2c_devices:main',
            'source_position = irradroom_python.source_position:main'
        ],
    },
)
