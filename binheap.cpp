#include <iostream>
#include <vector>

using namespace std;

void printLine() {
	cout << "---------------------------------------------------" << endl;
}

class BinomialTree {
public:
	int key;
	vector<BinomialTree*> siblings;
	BinomialTree* child;
	BinomialTree* parent;
	int degree;
	
	BinomialTree(int key) {
		this->key = key;
		this->child = NULL;
		this->parent = NULL;
		this->degree = 0;
	}

	void Print(bool sib) {
		cout << "({Key: " << this->key << ", Degree: " << this->degree << "})";
		if (sib) {
			for (int i = 0; i < this->siblings.size(); i++) {
				cout << " ";
				this->siblings[i]->Print(true);
			}
		}
		if (this->child != NULL) {
			cout << " ";
			this->child->Print(true);
		}
	}
};


class BinomialHeap {
public:
	vector<BinomialTree*> heap = vector<BinomialTree*>();
	BinomialHeap() {};

	BinomialTree* minimum() {
		BinomialTree* min = heap[0];
		for (int i = 1; i < heap.size(); i++) {
			if (heap[i]->key < min->key) {
				min = heap[i];
			}
		}
		return min;
	}
	// join two trees
	BinomialTree* binomialLink(BinomialTree* y, BinomialTree* z) {
		auto top = z;
		auto bottom = y;
		if (y->degree < z->degree) {
			top = y;
			bottom = z;
		}
		
		top->parent = nullptr;
		top->siblings.clear();
		
		bottom->parent = top;
		bottom->siblings.clear();

		if (top->child != NULL) {
			bottom->siblings.push_back(top->child);
			for (auto tree : top->child->siblings) {
				bottom->siblings.push_back(tree);
			}
		}
		top->child = bottom;
		top->degree++;
		return top;
	}

	vector<BinomialTree*> merge(BinomialHeap* h) {
		vector<BinomialTree*> newHeap = vector<BinomialTree*>();
		int it = 0, it2 = 0;
		while (true) {
			if (it >= heap.size() && it2 >= h->heap.size()) {
				break;
			}
			else if (it >= heap.size()) {
				newHeap.push_back(h->heap[it2++]);
				continue;
			}
			else if (it2 >= h->heap.size()) {
				newHeap.push_back(heap[it++]);
				continue;
			}
			if (heap[it]->degree < h->heap[it2]->degree) {
				newHeap.push_back(heap[it++]);
			}
			else {
				newHeap.push_back(h->heap[it2++]);
			}
		}
		return newHeap;
	}
	
	void Union(BinomialHeap* h) {
		auto newHeap = merge(h);
		int i = 0;
		while (i + 1 < newHeap.size()) {
			if (newHeap[i]->degree != newHeap[i + 1]->degree) {
				i++;
			}
			else {
				// 3 binomial trees with same degree
				if (i + 2 < newHeap.size() && newHeap[i]->degree == newHeap[i + 1]->degree && newHeap[i + 1]->degree == newHeap[i + 2]->degree) {
					auto tree = binomialLink(newHeap[i + 1], newHeap[i + 2]);
					newHeap[i + 1] = tree;
					newHeap.erase(newHeap.begin() + i +2 );
				}
				// 
				else {
					auto tree = binomialLink(newHeap[i], newHeap[i +1]);
					newHeap[i] = tree;
					newHeap.erase(newHeap.begin() + i + 1);
				}
			}
		}
		heap = newHeap;
	}

	void insert(int key) {
		auto h = new BinomialHeap();
		auto tree = new BinomialTree(key);
		h->heap.push_back(tree);
		Union(h);
	}

	void Print() {
		int i = 0;
		for (auto tree : heap) {
			cout << "Tree: " << i << endl;
			i++;
			tree->Print(true);
			cout << endl;
			printLine();
			cout << endl;
		}
	}

	BinomialHeap deleteMin(BinomialTree * tree) {
		BinomialHeap h;
		BinomialTree* temp = tree->child, * temp2;
		int i = 0;
		while (temp) {
			temp2 = temp;
			h.heap.insert(h.heap.begin(), temp2); //insert front
			if (temp->siblings.empty()) { //if no siblings then end
				break;
			}
			temp = temp->siblings[0]; 
			temp2->siblings.clear();
		}
		return h;
	}
	// Delete
	BinomialTree* extractMin() {
		BinomialHeap newHeap, h;
		BinomialTree* temp;
		auto it = heap.begin();
		temp = minimum();
		while (it != heap.end()) {
			if (*it != temp) newHeap.heap.push_back(*it);
			it++;
		}
		h = deleteMin(temp);
		h.Union(&newHeap);
		heap = h.heap;
		return temp;
	}
};

int main() {
	BinomialHeap* h;
	BinomialTree* tree;
	tree = new BinomialTree(10);
	h = new BinomialHeap();
	h->insert(1);
	h->insert(2);
	h->insert(3);
	h->insert(4);
	h->insert(5);
	h->insert(6);
	h->insert(7);
	h->Print();
	h->extractMin();
	h->Print();
}