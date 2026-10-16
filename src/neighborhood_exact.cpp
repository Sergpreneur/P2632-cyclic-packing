// Exhaustive local neighborhood checker: given 12 candidate ids, test if 13 is
// obtained by removing at most d of these 12 and adding d+1 compatible columns.
// No time caps, no heuristics: negative answers are exhaustive ONLY in these neighborhoods.
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <vector>
using namespace std;
struct R {array<unsigned long long,3> m{}; array<int,5> b{};};
vector<R> C;
vector<int> I;
uint64_t nodes;
bool disj(const R&a,const R&b){return !((a.m[0]&b.m[0])|(a.m[1]&b.m[1])|(a.m[2]&b.m[2]));}
bool disj(const array<unsigned long long,3>&a,const R&b){return !((a[0]&b.m[0])|(a[1]&b.m[1])|(a[2]&b.m[2]));}
bool dfs(const vector<int>&avail,int want, vector<int>&chosen){
  nodes++;
  if(want==0)return true;
  if(avail.size()<(size_t)want)return false;
  for(size_t j=0;j+want<=avail.size();j++){
    int a=avail[j];
    vector<int> nxt;nxt.reserve(avail.size()-j-1);
    for(size_t k=j+1;k<avail.size();k++)if(disj(C[a],C[avail[k]]))nxt.push_back(avail[k]);
    if(nxt.size()+1<(size_t)want)continue;
    chosen.push_back(a);
    if(dfs(nxt,want-1,chosen))return true;
    chosen.pop_back();
  }
  return false;
}
int main(int argc,char**argv){
  if(argc<4){cerr<<"Usage: neighborhood_exact candidates.tsv list_of_12_indices.txt max_drop\n";return 2;}
  ifstream f(argv[1]);string line;
  while(getline(f,line)){
    R r;string a,b;stringstream ss(line);getline(ss,a,'|');getline(ss,b);stringstream sa(a),sb(b);string t;
    int k=0;while(getline(sa,t,','))r.b[k++]=stoi(t);
    while(getline(sb,t,',')){int id=stoi(t);r.m[id/64]|=1ULL<<(id%64);}
    C.push_back(r);
  }
  if(C.size()!=4761)abort();
  ifstream g(argv[2]);int id;while(g>>id)I.push_back(id);
  if(I.size()!=12)abort();
  for(int d=1;d<=stoi(argv[3]);d++){
    auto begin=chrono::steady_clock::now();
    vector<int> choose(12,0);
    fill(choose.begin(),choose.begin()+d,1);
    int checked=0; nodes=0;
    do {
      array<unsigned long long,3> used={0,0,0}; vector<int> keep;
      for(int j=0;j<12;j++)if(!choose[j]){
        int k=I[j];keep.push_back(k);
        for(int t=0;t<3;t++)used[t]|=C[k].m[t];
      }
      vector<int> avail;avail.reserve(400);
      for(int k=0;k<(int)C.size();k++)if(disj(used,C[k]))avail.push_back(k);
      vector<int> chosen;
      if(dfs(avail,d+1,chosen)){
        cout<<"FOUND 13 by dropping "<<d<<" of the original 12.\n";
        for(int k:keep)cout<<"["<<C[k].b[0]<<","<<C[k].b[1]<<","<<C[k].b[2]<<","<<C[k].b[3]<<","<<C[k].b[4]<<"]\n";
        for(int k:chosen)cout<<"["<<C[k].b[0]<<","<<C[k].b[1]<<","<<C[k].b[2]<<","<<C[k].b[3]<<","<<C[k].b[4]<<"]\n";
        return 0;
      }
      checked++;
    }while(prev_permutation(choose.begin(),choose.end()));
    double dt=chrono::duration<double>(chrono::steady_clock::now()-begin).count();
    cout<<"EXHAUSTED drop="<<d<<" cases="<<checked<<" DFS_nodes="<<nodes<<" seconds="<<dt<<"\n"<<flush;
  }
  return 0;
}
