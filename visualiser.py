from curvatureSampler import CurvatureSampler
from equidistantSampler import EquidistantSampler
import matplotlib.pyplot as plt
from typing import Union
import csv
import os

class Visualiser:
    def __init__(self, sampler: Union[EquidistantSampler, CurvatureSampler]):
        self.sampler = sampler

    # Sample points from the entire shape
    def correct_shape(self, i, x_coords, y_coords):
        correctionV = abs(self.sampler.svgPathOperator.intersections_list[3][0].real - self.sampler.svgPathOperator.intersections_list[2][0].real)/2
        interesections = self.sampler.svgPathOperator.intersections_list
        if (i == self.sampler.svgPathOperator.svgPathReader.seperated_components[0]): # Maille
            for k in range(len(x_coords)):
                if  k == len(x_coords) -1 :
                    x_coords.append(x_coords[0])
                    y_coords.append(y_coords[0])

        if (i == self.sampler.svgPathOperator.svgPathReader.seperated_components[1]): # Connector Droit
            for k in range(len(x_coords)):
                print(f"length of the right connector is {len(x_coords)}")
                if  x_coords[k] <= interesections[0][0].real:
                    print("Correcting the CD")
                    x_coords[k] = interesections[0][0].real
                    y_coords[k] = -interesections[0][0].imag

        if (i == self.sampler.svgPathOperator.svgPathReader.seperated_components[2]): # Connector Gauche
            for k in range(len(x_coords)):
                print(f"length of the left connector is {len(x_coords)}")
                if  x_coords[k] >= interesections[1][0].real:
                    print("Correcting the CG")
                    x_coords[k] = interesections[1][0].real
                    y_coords[k] = -interesections[1][0].imag
        if (i == self.sampler.svgPathOperator.svgPathReader.seperated_components[3]): # Connector Haut
            for k in range(len(x_coords)):
                # if  y_coords[k] <= -self.sampler.svgPathOperator.intersections_list[2][0].imag:
                    print("Correcting the CH")
                    x_coords[k] = (interesections[2][0].real + correctionV) if interesections[2][0].real < interesections[3][0].real else (interesections[2][0].real - correctionV)
                    y_coords[k] = -interesections[2][0].imag
        if (i == self.sampler.svgPathOperator.svgPathReader.seperated_components[4]): # Connector Bas
            for k in range(len(x_coords)):
                # if  y_coords[k] >= -self.sampler.svgPathOperator.intersections_list[3][0].imag:
                    print("Correcting the CB")
                    x_coords[k] = (interesections[3][0].real + correctionV) if interesections[3][0].real < interesections[2][0].real else (interesections[3][0].real - correctionV)
                    y_coords[k] = -interesections[3][0].imag
                    
    
    def points_in_csv_file(self, sampler_name, i, x_coords, y_coords):
        full_path = f'{self.sampler.svgPathOperator.svgPathReader.imagePath}'
        folder_path = os.path.dirname(full_path)
        corrected_folder_path = folder_path.replace("/", "\\")
        print(corrected_folder_path)
        csv_file_name = f'{sampler_name}_{self.sampler.svgPathOperator.svgPathReader.dict_part_names[i]}_{self.sampler.svgPathOperator.svgPathReader.image_name}.csv'
        csv_file_path = os.path.join( corrected_folder_path, csv_file_name)
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['X', 'Y'])       
            for j in range (len(x_coords)):
                csv_writer.writerow([x_coords[j],y_coords[j]])


    def plot_shape(self, sampled_points):
        if isinstance(self.sampler, EquidistantSampler):           
            for i in range(len(self.sampler.svgPathOperator.svgPathReader.segments_list)):
                equidistant_points = self.sampler.my_equidistant_sampling(sampled_points, self.sampler.svgPathOperator.svgPathReader.segments_list[i])
                x_coords = [point.real for point in equidistant_points]
                y_coords = [-point.imag for point in equidistant_points]
                self.correct_shape(i, x_coords, y_coords)
                # Plot the sampled points
                self.points_in_csv_file('Equidistant_Sampling', i, x_coords, y_coords)
                plt.plot(x_coords, y_coords, color='blue', marker='.')
                
        if isinstance(self.sampler, CurvatureSampler): 
            for i in range(len(self.sampler.svgPathOperator.svgPathReader.bezier_curves_to_poly_list)):
                curvature_sampled_points = self.sampler.curvature_based_sampling(i, self.sampler.svgPathOperator.svgPathReader.bezier_curves_to_poly_list[i], sampled_points)
                x_coords = [point.real for point in curvature_sampled_points]
                y_coords = [-point.imag for point in curvature_sampled_points]
                self.correct_shape(i, x_coords, y_coords)
                self.points_in_csv_file('Curvature_Sampling', i, x_coords, y_coords)
                plt.plot(x_coords, y_coords, color='blue', marker='.')

        plt.axis('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Sampled Points from Bézier Curves')
        plt.grid(True)
        plt.show()


