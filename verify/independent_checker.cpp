// Independent O(31 * M * 10) exact verifier of a candidate cyclic packing.
// g++ -std=c++17 -O2 -o independent_checker independent_checker.cpp
// ./independent_checker certificates/constructions/packing_12.txt
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <set>
#include <vector>
using namespace std;
int main(int argc,char**argv){
  if(argc!=2){cerr<<"Usage: independent_checker packing_N.txt\n";return 2;}
  ifstream in(argv[1]); if(!in){cerr<<"file not found\n";return 2;}
  set<array<int,5>> translated;
  set<array<int,3>> seen;
  vector<array<int,5>> bases;
  array<int,5> b;
  while(in>>b[0]>>b[1]>>b[2]>>b[3]>>b[4]){
    for(auto v:b)if(v<0||v>=31){cerr<<"bad element\n";return 1;}
    sort(b.begin(),b.end());
    if(unique(b.begin(),b.end())!=b.end()){
      cerr<<"non-distinct elements in base block\n";return 1;
    }
    bases.push_back(b);
  }
  if(bases.empty()){cerr<<"no base blocks\n";return 1;}
  for(auto a:bases){
    for(int s=0;s<31;s++){
      array<int,5> x{};
      for(int i=0;i<5;i++)x[i]=(a[i]+s)%31;
      sort(x.begin(),x.end());
      if(!translated.insert(x).second){cerr<<"Repeated developed block\n";return 1;}
      for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)for(int k=j+1;k<5;k++){
        array<int,3> t={x[i],x[j],x[k]};
        if(!seen.insert(t).second){
          cerr<<"Repeated triple "<<t[0]<<" "<<t[1]<<" "<<t[2]<<"\n";
          return 1;
        }
      }
    }
  }
  if(translated.size()!=31*bases.size() || seen.size()!=310*bases.size())return 1;
  cout<<"PASS: base blocks="<<bases.size()<<" developed blocks="<<translated.size()
      <<" distinct triples="<<seen.size()<<" unused triples="<<(4495-seen.size())<<"\n";
  return 0;
}
