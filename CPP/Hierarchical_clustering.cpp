//
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <time.h>
#include <cmath>
#include <random>
#include <functional>
#include <chrono>

using namespace std;
using namespace std::chrono;	//Chrono library is used to deal with date and time.


double min_vals(double x, double y) {
	return min(x, y);
}

inline void min_col(vector<vector<double>>& distMatrix, int i_min, int j_min)
{
	int dist_mat_size = (int)distMatrix.size();

	for (int i = 0; i < dist_mat_size; i++) {
		double min_val = min(distMatrix[i][i_min], distMatrix[i][j_min]);
		if (min_val != -1) {
			distMatrix[i][i_min] = min_val; //update min value
			distMatrix[i][j_min] = -1; //flag value as merged, to be ignored later.
		}
	}
}

/*
Execute the Hierarchical Clustering.
*/
class HierarchicalClustering 
{

public:
	void test_matrix(vector<vector<double>>& distMatrix, int num_of_clusters) {

		init(distMatrix, num_of_clusters);

		auto start = high_resolution_clock::now();
		cout << "Clustering..." << endl;
		run_clustering();
		auto stop = high_resolution_clock::now();
		auto duration = duration_cast<chrono::milliseconds>(stop - start) / 1000.0;
		cout << "Loding File Complete Time: " << duration.count() << " [sec]" << endl;

	}

private:
	int n_clusters;
	int num_of_vectors;
	vector<vector<double>> distMatrix;
	vector<vector<int>> clusters;

	void init(vector<vector<double>> & distMatrix, int num_of_clusters)
	{
		this->distMatrix = distMatrix;
		this->num_of_vectors = (int)distMatrix.size();
		this->n_clusters = num_of_clusters;
		this->clusters.clear();
	}

	void run_clustering() 
	{
		int rows = (int)distMatrix.size();
		vector<double> nullvec(rows, -1); //tmp vec to replace row and col [merge]
		vector<double> init_vec(2);
		// initialize vec of vecs to be rowsX2
		vector<vector<double>> min_idx_val(rows, vector<double>(init_vec));
		clusters.resize(num_of_vectors);

		for (int i = 0; i < num_of_vectors; i++)
			distMatrix[i][i] = -1;

		for (int i = 0; i < num_of_vectors; i++)
			clusters[i].push_back({ i });

		// find minimal values and their indexes for each vector in matrix
		for (int i = 0; i < num_of_vectors; i++) 
		{
			double min_val = DBL_MAX;
			double min_j = 0;

			for (int j = 0; j < num_of_vectors; j++)
				if (distMatrix[i][j] != -1)
					if (distMatrix[i][j] < min_val) {
						min_val = distMatrix[i][j];
						min_j = j;
					}

			min_idx_val[i][0] = min_j;
			min_idx_val[i][1] = min_val;
		}

		int cnt = num_of_vectors;

		while (cnt > n_clusters) {

			int min_i = 0;
			double min_val = DBL_MAX;
			for (int i = 0; i < num_of_vectors; i++) {
				if (min_idx_val[i][1] != -1)
					if (min_idx_val[i][1] < min_val) {
						min_val = min_idx_val[i][1];
						min_i = i;
					}
			}
			int min_j = min_idx_val[min_i][0];   // update min index for j // [row][index/value]
			/////////////////////////Update the ////////////////////////////////////////
			transform(distMatrix[min_i].begin(), distMatrix[min_i].end(), distMatrix[min_j].begin(), distMatrix[min_i].begin(), min_vals);
			min_col(distMatrix, min_i, min_j);


			clusters[min_i].reserve(clusters[min_i].size() + clusters[min_j].size());
			clusters[min_i].insert(clusters[min_i].end(), clusters[min_j].begin(), clusters[min_j].end()); //add values to cluster
			clusters[min_j].clear();

			distMatrix[min_j] = nullvec; //mark as merged.
			min_idx_val[min_j] = { -1, -1 };
			for (int i = 0; i < num_of_vectors; i++) {
				if (min_idx_val[i][0] != -1 && min_idx_val[i][1])
					if (min_idx_val[i][0] == min_j)
						min_idx_val[i][0] = min_i;
			}

			min_val = DBL_MAX;   //find minimal value in vector
			for (int i = 0; i < num_of_vectors; i++) {
				if (distMatrix[min_i][i] != -1)
					if (distMatrix[min_i][i] < min_val) {
						min_val = distMatrix[min_i][i];
						min_j = i;
					}
			}
			// update vector min_i with minimal value and it's index
			min_idx_val[min_i][0] = min_j;
			min_idx_val[min_i][1] = distMatrix[min_i][min_j];

			cnt--;
		}
	}
};

/*
VecMatrix getDistanceMatrix(string file_name) - This function is read from a file the distance matrix.
Input - File name.
Output - Distancne matrix.
*/
vector<vector<double>> getDistanceMatrix(string file)
{
	vector<vector<double>> distMatrix;
	ifstream ifs(file);
	string tempstr;

	double tempint;
	char delimiter;

	while (getline(ifs, tempstr)) 
	{
		istringstream iss(tempstr);
		vector<double> tempv;
		while (iss >> tempint) 
		{
			tempv.push_back(tempint);
			iss >> delimiter;
		}
		distMatrix.push_back(tempv);
	}
	return distMatrix;
	
}

/*
testFromFile - Function the called from the main,
and responsible to operate all the program.
*/
void testFromFile(string file, size_t n_clusters)
{
	cout << "Loding File " << endl;
	auto start = high_resolution_clock::now();
	vector<vector<double>> distMatrix = getDistanceMatrix(file);
	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<chrono::milliseconds>(stop - start) / 1000.0;
	cout << "Loding File Complete Time: " << duration.count() << " [sec]" << endl;
	cout << endl;

	cout << "Hierarchical clustering of distance matrix " << endl;
	// Call the class, and start clustering
	HierarchicalClustering hierarchical_clustering;
	hierarchical_clustering.test_matrix(distMatrix, n_clusters);
	cout << "===================================================" << endl << endl;
}

/*
Our main program executaion.
*/
int main()
{
	size_t n_clusters = 2;
	testFromFile("data_2_4.txt", n_clusters);

	return 0;
}




