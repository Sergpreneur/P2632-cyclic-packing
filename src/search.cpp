// Heuristic + bounded local exact search for mutually disjoint cyclic triple-orbit resources.
// Compile: g++ -O3 -std=c++17 -o search src/search.cpp
// Usage: search <root_dir> <seconds> <seed>
#include <bits/stdc++.h>
using namespace std;
struct Row {
    array<uint64_t,3> m={0,0,0};
    array<int,10> rr{};
    vector<int> blk;
};
vector<Row> rows;
mt19937_64 rng;
long long nodes=0, limit_nodes=0;
int best_size=0;
vector<int> best, current;
string root;
bool disj(const array<uint64_t,3>&a,const array<uint64_t,3>&b) {
    return !((a[0]&b[0]) | (a[1]&b[1]) | (a[2]&b[2]));
}
void merge_mask(array<uint64_t,3>&a,const array<uint64_t,3>&b) {
    a[0]|=b[0];a[1]|=b[1];a[2]|=b[2];
}
void load_data() {
    ifstream in(root+"/data/candidates.tsv");
    string line;
    while(getline(in,line)){
        Row c;
        stringstream ss(line);
        string block,res;
        getline(ss,block,'|');getline(ss,res,'|');
        stringstream bs(block),rs(res);string t;
        while(getline(bs,t,','))c.blk.push_back(stoi(t));
        int j=0;
        while(getline(rs,t,',')){
            int r=stoi(t);c.rr[j++]=r;c.m[r/64]|=1ULL<<(r%64);
        }
        if(j!=10)abort();
        rows.push_back(c);
    }
    if(rows.size()!=4761)abort();
}
int pick_int(int n) { return (int)(rng()%n); }
void save_best(const vector<int>&c) {
    if((int)c.size()<=best_size)return;
    array<uint64_t,3> m={0,0,0};
    for(int i:c){if(!disj(m,rows[i].m))abort();merge_mask(m,rows[i].m);}
    best=c;best_size=c.size();
    cerr<<"BEST "<<best_size<<" seed "<<rng()<<" nodes "<<nodes<<"\n";
    ofstream out(root+"/experiments/checkpoints/search_best.json");
    out<<"{\"blocks\":[";
    for(size_t i=0;i<c.size();i++) {
        if(i)out<<",";
        out<<"[";
        for(int j=0;j<5;j++)out<<(j?",":"")<<rows[c[i]].blk[j];
        out<<"]";
    }
    out<<"],\"candidate_indices\":[";
    for(size_t i=0;i<c.size();i++)out<<(i?",":"")<<c[i];
    out<<"]}\n";
}
bool dfs(const vector<int>&av,int target,vector<int>&chosen) {
    if(target<=0)return true;
    if((int)av.size()<target || nodes++>limit_nodes)return false;
    // Cheap necessary condition: at least 10*target distinct resources occur among choices
    if(target==1) {chosen.push_back(av[0]);return true;}
    for(size_t i=0;i+target<=av.size();i++){
        int a=av[i];
        vector<int> next;
        next.reserve(av.size()-i);
        for(size_t j=i+1;j<av.size();j++)
            if(disj(rows[a].m,rows[av[j]].m))next.push_back(av[j]);
        if((int)next.size()+1<target)continue;
        chosen.push_back(a);
        if(dfs(next,target-1,chosen))return true;
        chosen.pop_back();
        if(nodes>limit_nodes)break;
    }
    return false;
}
vector<int> avail_given(const vector<int>&fixed) {
    array<uint64_t,3> used={0,0,0};
    for(int i:fixed)merge_mask(used,rows[i].m);
    vector<int> av;
    for(int i=0;i<(int)rows.size();i++)if(disj(used,rows[i].m))av.push_back(i);
    return av;
}
void order_avail(vector<int>&av) {
    // Greedy select constrained low-overlap columns: static frequencies among available resources.
    int freq[145]={};
    for(int i:av)for(int r:rows[i].rr)freq[r]++;
    vector<pair<double,int>> order;
    order.reserve(av.size());
    for(int i:av){
        double cost=0;
        for(int r:rows[i].rr)cost+=freq[r];
        double noise=(double)(rng()%1000000)/1000000.0;
        cost *= (0.55+noise*1.10);
        order.emplace_back(cost,i);
    }
    sort(order.begin(),order.end());
    for(int j=0;j<(int)av.size();j++)av[j]=order[j].second;
}
vector<int> randomized_greedy() {
    vector<int> avail(rows.size());iota(avail.begin(),avail.end(),0);
    vector<int> out;
    array<uint64_t,3> used={0,0,0};
    while(!avail.empty()) {
        order_avail(avail);
        int n=min((int)avail.size(),1+pick_int(18));
        // pick a low cost candidate from top-n to allow variance
        int ix=avail[pick_int(n)];
        out.push_back(ix);merge_mask(used,rows[ix].m);
        vector<int> next;
        for(int i:avail)if(disj(rows[i].m,used))next.push_back(i);
        avail=move(next);
    }
    return out;
}
vector<int> read_indices(const string&f) {
    ifstream in(f);
    string s((istreambuf_iterator<char>(in)),{});
    // Read the id list embedded in JSON, if present.
    auto pos=s.find("candidate_indices");
    if(pos==string::npos)return {};
    pos=s.find('[',pos);auto end=s.find(']',pos);
    if(end==string::npos)return {};
    vector<int> out; stringstream ss(s.substr(pos+1,end-pos-1)); string t;
    while(getline(ss,t,','))if(!t.empty())out.push_back(stoi(t));
    return out;
}
int main(int argc,char**argv) {
    if(argc<4){cerr<<"Usage: search root seconds seed [start_checkpoint]\n";return 1;}
    root=argv[1];auto deadline=chrono::steady_clock::now()+chrono::milliseconds((int)(stod(argv[2])*1000));
    uint64_t seed=strtoull(argv[3],nullptr,10);rng.seed(seed);
    load_data();
    vector<int> incumbent=read_indices(root+"/data/best_packing.json");
    if(argc>4)incumbent=read_indices(argv[4]);
    if(!incumbent.empty()){save_best(incumbent);current=incumbent;}
    long long iters=0, replacements=0;
    while(chrono::steady_clock::now()<deadline) {
        iters++;
        if((iters%400==0)||current.empty())current=randomized_greedy();
        if(current.size()>=best_size)save_best(current);
        int k=current.size();
        if(k<2)continue;
        int d=1+pick_int(min(k,7));
        // Bias towards moderate disturbance.
        if(k>=10 && pick_int(10)<7)d=2+pick_int(min(k-1,5));
        auto subset=current;shuffle(subset.begin(),subset.end(),rng);
        vector<int> keep(subset.begin()+d,subset.end());
        vector<int> av=avail_given(keep);
        order_avail(av);
        vector<int> selected;
        nodes=0;
        limit_nodes=5000+(pick_int(20)==0?150000:0);
        bool improved=dfs(av,d+1,selected);
        if(improved){
            keep.insert(keep.end(),selected.begin(),selected.end());
            current=keep;
            save_best(current);
            replacements++;
            continue;
        }
        if(pick_int(100)<77){
            selected.clear();nodes=0;limit_nodes=1000;
            if(dfs(av,d,selected)){
                keep.insert(keep.end(),selected.begin(),selected.end());
                current=keep; replacements++;
                continue;
            }
        }
        // Walk on slightly smaller solutions to exit local maxima
        if(pick_int(100)<15){
            selected.clear();nodes=0;limit_nodes=400;
            if(d>1 && dfs(av,d-1,selected)){
                keep.insert(keep.end(),selected.begin(),selected.end());
                current=keep;replacements++;
            }
        }
    }
    cerr<<"DONE seed "<<seed<<" iterations "<<iters<<" replacements "<<replacements<<" best "<<best_size<<"\n";
}
