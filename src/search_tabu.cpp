// Tabu-min-conflicts for 13 orbit classes: objective repeated triple-orbit resources.
// usage: search_tabu <root> <seconds> <seed>
#include <bits/stdc++.h>
using namespace std;
struct Row{array<int,10> rr;vector<int> block;};
vector<Row> rows;
mt19937_64 rng;
int rnd(int n){return rng()%n;}
void load(string root){
    ifstream in(root+"/data/candidates.tsv");string line;
    while(getline(in,line)){
        Row a; string lhs,rhs;stringstream ss(line);getline(ss,lhs,'|');getline(ss,rhs,'|');
        stringstream b(lhs),r(rhs);string x;
        while(getline(b,x,','))a.block.push_back(stoi(x));
        int j=0;while(getline(r,x,','))a.rr[j++]=stoi(x);
        if(j!=10) abort();rows.push_back(a);
    }
}
void save(string root,vector<int>&v,int energy,int iter,uint64_t seed){
    ofstream f(root+"/experiments/checkpoints/tabu_"+to_string(v.size())+".json");
    f<<"{\"blocks\":[";
    for(int i=0;i<(int)v.size();i++){
        f<<(i?",":"")<<"[";
        for(int j=0;j<5;j++)f<<(j?",":"")<<rows[v[i]].block[j];
        f<<"]";
    }
    f<<"],\"candidate_indices\":[";
    for(int i=0;i<(int)v.size();i++)f<<(i?",":"")<<v[i];
    f<<"],\"energy\":"<<energy<<",\"iterations\":"<<iter<<",\"seed\":"<<seed<<"}\n";
}
int main(int argc,char**argv){
    if(argc<4)return 1;
    string root=argv[1];double seconds=stod(argv[2]);uint64_t seed=stoull(argv[3]);rng.seed(seed);
    load(root);
    auto deadline=chrono::steady_clock::now()+chrono::milliseconds(int(seconds*1000));
    const int K=13,NUM=rows.size();
    vector<int> current(K),tabu(NUM,0);int counts[145]={};
    int initial[]={1376,816,4695,3486,291,3087,3730,4577,1226,1682,4220,3597};
    for(int i=0;i<12;i++)current[i]=initial[i];
    int init13=-1,ic=11;
    for(int i=0;i<NUM;i++){
        int count=0;
        for(int x:rows[i].rr){
            bool found=false;
            for(int j=0;j<12;j++)for(int y:rows[current[j]].rr)if(x==y)found=true;
            if(found)count++;
        }
        if(count<ic){ic=count;init13=i;}
    }
    current[12]=init13;
    for(int i:current)for(int r:rows[i].rr)counts[r]++;
    int energy=0;for(int r=0;r<145;r++)energy+=max(0,counts[r]-1);
    int best=energy,iteration=0,nrestarts=0;
    vector<int> saved=current;
    cerr<<"INITIAL energy "<<energy<<"\n";
    save(root,current,energy,iteration,seed);
    while(chrono::steady_clock::now()<deadline){
        iteration++;
        if(iteration%12000==0){
            // Restart from near-optimal or exploratory packed subsets.
            nrestarts++;
            current=saved;
            for(int j=0;j<K;j++)if(rnd(3)==0)current[j]=rnd(NUM);
            fill(begin(counts),end(counts),0);
            for(int i:current)for(int r:rows[i].rr)counts[r]++;
            energy=0;for(int r=0;r<145;r++)energy+=max(0,counts[r]-1);
            fill(tabu.begin(),tabu.end(),0);
        }
        int slot=rnd(K);
        int old=current[slot];
        for(int r:rows[old].rr)counts[r]--;
        int base=0;for(int r=0;r<145;r++)base+=max(0,counts[r]-1);
        int min_val=999,chosen=-1,cands=0;
        int turn=iteration;
        // Global-move evaluation for a random slot, all candidate columns.
        // Random tie break + tabu relaxation if no eligible move.
        int offset=rnd(NUM);
        for(int tt=0;tt<NUM;tt++){
            int j=(tt+offset)%NUM;
            if(j==old)continue;
            int extra=0;
            for(int r:rows[j].rr)extra+=(counts[r]>0);
            if(tabu[j]>turn && base+extra>=best)continue;
            if(extra<min_val){min_val=extra;chosen=j;cands=1;}
            else if(extra==min_val && rnd(++cands)==0)chosen=j;
            if(extra==0 && base==0)break;
        }
        if(chosen==-1){chosen=old;min_val=energy-base;}
        current[slot]=chosen;
        for(int r:rows[chosen].rr)counts[r]++;
        energy=base+min_val;
        tabu[old]=turn+5+rnd(65);
        if(energy<best){
            best=energy;saved=current;
            cerr<<"BEST energy "<<best<<" iter "<<iteration<<" restarts "<<nrestarts<<"\n";
            save(root,current,energy,iteration,seed);
            if(best==0)break;
        }
    }
    cerr<<"DONE seed "<<seed<<" iter "<<iteration<<" restarts "<<nrestarts<<" min-energy "<<best<<"\n";
}
