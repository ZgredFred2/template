#include <bits/stdc++.h>
using namespace std;

#if defined(LOCAL)
	#define what_is(x) cout<<(#x)<<": "<<(x)<<endl;
#else
	#define what_is(x) ;
#endif

#if defined(LOCAL)
	#define dprintf printf
#else
	#define dprintf(...) ;
#endif

using ll = long long;
using db = long double;
using str = string;
 
using pi = pair<int,int>;
using pl = pair<ll,ll>;
using pd = pair<db,db>;
 
using vi = vector<int>;
using vb = vector<bool>;
using vl = vector<ll>;
using vd = vector<db>; 
using vs = vector<str>;
using vpi = vector<pi>;
using vpl = vector<pl>;
using vpd = vector<pd>;

// pairs
#define mp make_pair
#define f first
#define s second

// vectors
#define sz(x) int((x).size())
#define bg(x) begin(x)
#define all(x) bg(x), end(x)
#define rall(x) x.rbegin(), x.rend() 
#define sor(x) sort(all(x)) 
#define rsz resize
#define ins insert 
#define ft front()
#define bk back()
#define pb push_back
#define eb emplace_back 
#define pf push_front
#define ret return

#define lb lower_bound
#define ub upper_bound

// option
#define option optional
#define hv has_value()
#define vv value()


inline namespace my_lib{
	template<typename T> bool ckmin(T& a, const T& b) {
		return b < a ? a = b, 1 : 0; } // set a = min(a,b)
	template<typename T> bool ckmax(T& a, const T& b) {
		return a < b ? a = b, 1 : 0; }
}

inline namespace my_numeric{
	const ll max_ll=numeric_limits<ll>::max();
	const int max_int=numeric_limits<int>::max();
}

inline namespace my_iostream{
	#define fsh fflush(stdout);
	ostream& operator<<(ostream& os, const pair<auto,auto> &p);
	ostream& operator<<(ostream& os, const option<auto> &o);
	ostream& operator<<(ostream& os, const vector<auto>& v);
	ostream& operator<<(ostream& os, const map<auto,auto>& m);
	ostream& operator<<(ostream& os, const set<auto>& s);

	// printf("%s", to_str(thing).c_str()) NOT EFFICIENT, DEBUG PURPOSE
	string to_str(const auto &p);
	#define ts(x) to_str(x).c_str()

	// cout << pair<*,*>
	ostream& operator<<(ostream& os, const pair<auto,auto> &p){
		os<<"("<<p.f<<", "<<p.s<<")";
	    return os;
	}

	// cout << option<*>
	ostream& operator<<(ostream& os, const option<auto> &o){
		if(o.has_value()){
			os<<o.value();
		}else{
			os<<"empty";
		}
	    return os;
	}

	// cout << vector<*>
	ostream& operator<<(ostream& os, const vector<auto>& v){
		os<<"[";for (int i = 0; i < (int)v.size(); ++i){
	    	if(i) os<<", ";	
	    	os<<v[i];
	    }os<<"]";
	    return os;
	}

	// cout << map<*,*>
	ostream& operator<<(ostream& os, const map<auto,auto>& m){
		os<<"[";for (auto it = m.cbegin(); it!=m.cend(); ++it){
	    	if(it!=m.cbegin()) os<<", ";	
	    	os<< it->first << "=>" << it->second;
	    }os<<"]";
	    return os;
	}

	// cout << set<*>
	ostream& operator<<(ostream& os, const set<auto>& s){
		os<<"[";for (auto it = s.begin(); it!=s.end(); ++it){
	    	if(it!=s.begin()) os<<", ";
	    	os<< *it;
	    }os<<"]";
	    return os;
	}

	string to_str(const auto &p){
		ostringstream oss;
		oss << p;
		return oss.str();
	}
}

inline namespace MyTuples{
	template<typename A, typename B, typename C>
	struct Tri{
		A a;
		B b;
		C c;
		bool operator<(const Tri<auto,auto,auto> &o)const{
			return (a!=o.a)
				? (a<o.a)
				: ((b!=o.b)
					? (b<o.b)
					: ((c!=o.c)
						? (c<o.c)
						: 0));
		}
	};

	ostream& operator<<(ostream& os, const Tri<auto,auto,auto>& e){
		os<<"("<<e.a<<","<<e.b<<","<<e.c<<")";
	    return os;
	}

	template<typename A,typename B, typename C,typename D>
	struct Quad{
		A a;
		B b;
		C c;
		D d;
		bool operator<(const Quad<auto,auto,auto,auto> &o)const{
			return (a!=o.a)
				? (a<o.a)
				: ((b!=o.b)
					? (b<o.b)
					: ((c!=o.c)
						? (c<o.c)
						: ((d!=o.d)
							? (d<o.d)
							: 0)));
		}
	};

	ostream& operator<<(ostream& os, const Quad<auto,auto,auto,auto>& e){
		os<<"("<<e.a<<","<<e.b<<","<<e.c<<","<<e.d<<")";
	    return os;
	}

	template<typename A,typename B, typename C,typename D, typename E>
	struct Fifs{
		A a;
		B b;
		C c;
		D d;
		E e;
		bool operator<(const Fifs<auto,auto,auto,auto,auto> &o)const{
			return (a!=o.a)
				? (a<o.a)
				: ((b!=o.b)
					? (b<o.b)
					: ((c!=o.c)
						? (c<o.c)
						: ((d!=o.d)
							? (d<o.d)
							: ((e!=o.e)
								? (e<o.e)
								: 0))));
		}
	};

	ostream& operator<<(ostream& os, const Fifs<auto,auto,auto,auto,auto>& e){
		os<<"("<<e.a<<","<<e.b<<","<<e.c<<","<<e.d<<","<<e.e<<")";
	    return os;
	}

	struct Integer{
		int v;
		operator int&(){
			return v;
		}
		int &operator=(const int &o){
			v=o;
			return v;
		}
		bool operator==(const int& o)const {
			return v==o;
		}
	};

	ostream& operator<<(ostream& os, const Integer& e){
		os<<e.v;
	    return os;
	}
}

inline namespace my_read{
	int read_int(){
		int a;
		scanf("%d",&a);
		return a;
	}

	ll read_ll(){
		ll a;
		scanf("%lld", &a);
		return a;
	}

	float read_float(){
		float f;
		scanf("%f",&f);
		return f;
	}

	double read_double(){
		double lf;
		scanf("%lf", &lf);
		return lf;
	}

	pi read_pi(){
		pi p;
		scanf("%d%d",&p.f, &p.s);
		return p;
	}

	pl read_pl(){
		pl p;
		scanf("%lld%lld", &p.f, &p.s);
		return p;
	}

	char read_char(){
		char c;
		cin >> c;
		return c;
	}
}

const int MX=1*1e5+30;

int main(){
	int T = read_int();
	for (int test = 0; test < T; ++test){
		
	}
}