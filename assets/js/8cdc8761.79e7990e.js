"use strict";(self.webpackChunkdocs_v_2=self.webpackChunkdocs_v_2||[]).push([[2255],{3905:function(e,t,n){n.d(t,{Zo:function(){return d},kt:function(){return k}});var a=n(7294);function l(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function r(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?r(Object(n),!0).forEach((function(t){l(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):r(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function p(e,t){if(null==e)return{};var n,a,l=function(e,t){if(null==e)return{};var n,a,l={},r=Object.keys(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||(l[n]=e[n]);return l}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(l[n]=e[n])}return l}var o=a.createContext({}),i=function(e){var t=a.useContext(o),n=t;return e&&(n="function"==typeof e?e(t):s(s({},t),e)),n},d=function(e){var t=i(e.components);return a.createElement(o.Provider,{value:t},e.children)},c={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},u=a.forwardRef((function(e,t){var n=e.components,l=e.mdxType,r=e.originalType,o=e.parentName,d=p(e,["components","mdxType","originalType","parentName"]),u=i(n),k=l,m=u["".concat(o,".").concat(k)]||u[k]||c[k]||r;return n?a.createElement(m,s(s({ref:t},d),{},{components:n})):a.createElement(m,s({ref:t},d))}));function k(e,t){var n=arguments,l=t&&t.mdxType;if("string"==typeof e||l){var r=n.length,s=new Array(r);s[0]=u;var p={};for(var o in t)hasOwnProperty.call(t,o)&&(p[o]=t[o]);p.originalType=e,p.mdxType="string"==typeof e?e:l,s[1]=p;for(var i=2;i<r;i++)s[i]=n[i];return a.createElement.apply(null,s)}return a.createElement.apply(null,n)}u.displayName="MDXCreateElement"},5126:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return p},contentTitle:function(){return o},metadata:function(){return i},toc:function(){return d},default:function(){return u}});var a=n(7462),l=n(3366),r=(n(7294),n(3905)),s=["components"],p={sidebar_label:"graph",title:"graph"},o=void 0,i={unversionedId:"reference/graph",id:"reference/graph",isDocsHomePage:!1,title:"graph",description:"Handles creation and ops for DAGs",source:"@site/docs/reference/graph.md",sourceDirName:"reference",slug:"/reference/graph",permalink:"/spock/reference/graph",editUrl:"https://github.com/fidelity/spock/edit/master/website/docs/reference/graph.md",tags:[],version:"current",frontMatter:{sidebar_label:"graph",title:"graph"},sidebar:"api",previous:{title:"exceptions",permalink:"/spock/reference/exceptions"},next:{title:"handlers",permalink:"/spock/reference/handlers"}},d=[{value:"BaseGraph Objects",id:"basegraph-objects",children:[]},{value:"MergeGraph Objects",id:"mergegraph-objects",children:[]},{value:"SelfGraph Objects",id:"selfgraph-objects",children:[]},{value:"VarGraph Objects",id:"vargraph-objects",children:[]},{value:"Graph Objects",id:"graph-objects",children:[]}],c={toc:d};function u(e){var t=e.components,n=(0,l.Z)(e,s);return(0,r.kt)("wrapper",(0,a.Z)({},c,n,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("p",null,"Handles creation and ops for DAGs"),(0,r.kt)("h2",{id:"basegraph-objects"},"BaseGraph Objects"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class BaseGraph(ABC)\n")),(0,r.kt)("p",null,"Class that holds graph methods"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"_dag")," - graph of the dependencies between spock classes")),(0,r.kt)("h4",{id:"__init__"},"_","_","init","_","_"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(dag: Dict, whoami: str)\n")),(0,r.kt)("p",null,"Init call for Graph class"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"dag")," - a directed acyclic graph as a dictionary (keys -",">"," nodes, values -",">"," edges)"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"whoami")," - str value of whom the caller is")),(0,r.kt)("h4",{id:"dag"},"dag"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef dag()\n")),(0,r.kt)("p",null,"Returns the DAG"),(0,r.kt)("h4",{id:"nodes"},"nodes"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\n@abstractmethod\ndef nodes()\n")),(0,r.kt)("p",null,"Returns the nodes"),(0,r.kt)("h4",{id:"node_names"},"node","_","names"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef node_names()\n")),(0,r.kt)("p",null,"Returns the node names"),(0,r.kt)("h4",{id:"node_map"},"node","_","map"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef node_map()\n")),(0,r.kt)("p",null,"Returns a map of the node names to the underlying classes"),(0,r.kt)("h4",{id:"reverse_map"},"reverse","_","map"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef reverse_map()\n")),(0,r.kt)("p",null,"Returns a map from the underlying classes to the node names"),(0,r.kt)("h4",{id:"roots"},"roots"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef roots()\n")),(0,r.kt)("p",null,"Returns the roots of the dependency graph"),(0,r.kt)("h4",{id:"topological_order"},"topological","_","order"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef topological_order()\n")),(0,r.kt)("p",null,"Returns the topological sort of the DAG"),(0,r.kt)("h4",{id:"_build"},"_","build"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@abstractmethod\ndef _build() -> Dict\n")),(0,r.kt)("p",null,"Builds a dictionary of nodes and their edges (essentially builds the DAG)"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  dictionary of nodes and their edges"),(0,r.kt)("h4",{id:"_has_cycles"},"_","has","_","cycles"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _has_cycles() -> bool\n")),(0,r.kt)("p",null,"Uses DFS to check for cycles within the given graph"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  boolean if a cycle is found"),(0,r.kt)("h4",{id:"_cycle_dfs"},"_","cycle","_","dfs"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _cycle_dfs(node: str, visited: Dict, recursion_stack: Dict) -> bool\n")),(0,r.kt)("p",null,"DFS via a recursion stack for cycles"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"node")," - current graph node (spock class type)"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"visited")," - dictionary of visited nodes"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"recursion_stack")," - dictionary that is the recursion stack that is used to find cycles")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  boolean if a cycle is found"),(0,r.kt)("h4",{id:"_topological_sort"},"_","topological","_","sort"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _topological_sort() -> List\n")),(0,r.kt)("p",null,"Topologically sorts the DAG"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  list of topological order"),(0,r.kt)("h4",{id:"_topological_sort_dfs"},"_","topological","_","sort","_","dfs"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _topological_sort_dfs(node: str, visited: Dict, stack: List) -> None\n")),(0,r.kt)("p",null,"Depth first search"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"node")," - current node"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"visited")," - visited nodes"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"stack")," - order of graph")),(0,r.kt)("h2",{id:"mergegraph-objects"},"MergeGraph Objects"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class MergeGraph(BaseGraph)\n")),(0,r.kt)("p",null,"Class that allows for merging of multiple graphs"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"_input_classes")," - list of input classes that link to a backend"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"_args")," - variable nuber of graphs to merge"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"_dag")," - graph of the dependencies between spock classes")),(0,r.kt)("h4",{id:"__init__-1"},"_","_","init","_","_"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(*args: Dict, *, input_classes: List)\n")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"*args")," - variable number of graphs to merge"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"input_classes")," - list of input classes that link to a backend")),(0,r.kt)("h4",{id:"_merge_inputs"},"_","merge","_","inputs"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@staticmethod\ndef _merge_inputs(*args: Dict)\n")),(0,r.kt)("p",null,"Merges multiple graphs into a single dependency graph"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"*args")," - variable number of graphs to merge")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  dictionary of the merged dependency graphs"),(0,r.kt)("h4",{id:"nodes-1"},"nodes"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef nodes()\n")),(0,r.kt)("p",null,"Returns the input_classes/nodes"),(0,r.kt)("h4",{id:"_build-1"},"_","build"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _build() -> Dict\n")),(0,r.kt)("p",null,"Builds a dictionary of nodes and their edges (essentially builds the DAG)"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  dictionary of nodes and their edges"),(0,r.kt)("h2",{id:"selfgraph-objects"},"SelfGraph Objects"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class SelfGraph(BaseGraph)\n")),(0,r.kt)("h4",{id:"node_map-1"},"node","_","map"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef node_map()\n")),(0,r.kt)("p",null,"Returns a map of the node names to the underlying classes"),(0,r.kt)("h4",{id:"reverse_map-1"},"reverse","_","map"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef reverse_map()\n")),(0,r.kt)("p",null,"Returns a map from the underlying classes to the node names"),(0,r.kt)("h4",{id:"_build-2"},"_","build"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _build() -> Tuple[Dict, Dict]\n")),(0,r.kt)("p",null,"Builds a dictionary of nodes and their edges (essentially builds the DAG)"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  dictionary of nodes and their edges"),(0,r.kt)("h2",{id:"vargraph-objects"},"VarGraph Objects"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class VarGraph(BaseGraph)\n")),(0,r.kt)("p",null,"Class that helps with variable resolution by mapping dependencies"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"_input_classes")," - list of input classes that link to a backend"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"_cls_fields_tuple")," - tuple of cls and the given field dict"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"_dag")," - graph of the dependencies between spock classes"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"var_resolver")," - cls instance of the variable resolver"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"ref_map")," - dictionary of the references that need to be mapped to a value")),(0,r.kt)("h4",{id:"__init__-2"},"_","_","init","_","_"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(cls_fields_list: List[Tuple[_C, Dict]], input_classes: List)\n")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"cls_fields_list")," - tuple of cls and the given field dict"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"input_classes")," - list of input classes that link to a backend")),(0,r.kt)("h4",{id:"cls_names"},"cls","_","names"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef cls_names()\n")),(0,r.kt)("p",null,"Returns the set of class names"),(0,r.kt)("h4",{id:"cls_values"},"cls","_","values"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef cls_values()\n")),(0,r.kt)("p",null,"Returns a map of the class name and the underlying classes"),(0,r.kt)("h4",{id:"cls_map"},"cls","_","map"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef cls_map()\n")),(0,r.kt)("p",null,"Returns a map between the class names and the field dictionaries"),(0,r.kt)("h4",{id:"nodes-2"},"nodes"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef nodes()\n")),(0,r.kt)("p",null,"Returns the input_classes/nodes"),(0,r.kt)("h4",{id:"ref_2_resolve"},"ref","_","2","_","resolve"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef ref_2_resolve() -> Set\n")),(0,r.kt)("p",null,"Returns the values that need to be resolved"),(0,r.kt)("h4",{id:"_cast_all_maps"},"_","cast","_","all","_","maps"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _cast_all_maps(cls_name: str, changed_vars: Set) -> None\n")),(0,r.kt)("p",null,"Casts all the resolved references to the requested type"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"cls_name")," - name of the underlying class"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"changed_vars")," - set of resolved variables that need to be cast")),(0,r.kt)("h4",{id:"resolve"},"resolve"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def resolve(spock_cls: str, spock_space: Dict) -> Dict\n")),(0,r.kt)("p",null,"Resolves variable references by searching thorough the current spock_space"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"spock_cls")," - name of the spock class"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"spock_space")," - current spock_space to look for the underlying value")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  field dictionary containing the resolved values"),(0,r.kt)("h4",{id:"_build-3"},"_","build"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _build() -> Tuple[Dict, Dict]\n")),(0,r.kt)("p",null,"Builds a dictionary of nodes and their edges (essentially builds the DAG)"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  tuple of dictionary of nodes and their edges and well as the dictionary\nmap between the references"),(0,r.kt)("h2",{id:"graph-objects"},"Graph Objects"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class Graph(BaseGraph)\n")),(0,r.kt)("p",null,"Class that holds graph methods for determining dependencies between spock classes"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"_input_classes")," - list of input classes that link to a backend"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"_dag")," - graph of the dependencies between spock classes"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"_lazy")," - attempts to lazily find @spock decorated classes registered within\nsys.modules",'["',"spock",'"]',".backend.config")),(0,r.kt)("h4",{id:"__init__-3"},"_","_","init","_","_"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(input_classes: List, lazy: bool)\n")),(0,r.kt)("p",null,"Init call for Graph class"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"input_classes")," - list of input classes that link to a backend"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"lazy")," - attempts to lazily find @spock decorated classes registered within\nsys.modules",'["',"spock",'"]',".backend.config")),(0,r.kt)("h4",{id:"nodes-3"},"nodes"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef nodes()\n")),(0,r.kt)("p",null,"Returns the input_classes/nodes"),(0,r.kt)("h4",{id:"_yield_class_deps"},"_","yield","_","class","_","deps"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@staticmethod\ndef _yield_class_deps(classes: Union[List, Tuple]) -> Generator[Tuple, None, None]\n")),(0,r.kt)("p",null,"Generator to iterate through nodes and find dependencies"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"classes")," - list or tuple of classes to iterate through")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Yields"),":"),(0,r.kt)("p",null,"  tuple or the base input class and the current name of the dependent class"),(0,r.kt)("h4",{id:"_lazily_find_classes"},"_","lazily","_","find","_","classes"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _lazily_find_classes(classes: List) -> Tuple\n")),(0,r.kt)("p",null,"Searches within the spock sys modules attributes to lazily find @spock\ndecorated classes"),(0,r.kt)("p",null,"These classes have been decorated with @spock but might not have been passes\ninto the ConfigArgBuilder so\nthis allows for ","'","lazy","'"," lookup of these classes to make the call to\nConfigArgBuilder a little less verbose\nwhen there are a lot of spock classes"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  tuple of any lazily discovered classes"),(0,r.kt)("h4",{id:"_lazily_find_parents"},"_","lazily","_","find","_","parents"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _lazily_find_parents() -> Tuple\n")),(0,r.kt)("p",null,"Searches within the current set of input_classes (@spock decorated classes)\nto lazily find any parents"),(0,r.kt)("p",null,"Given that lazy inheritance means that the parent classes won","'","t be included\n(since they are cast to spock\nclasses within the decorator and the MRO is handled internally) this allows\nthe lazy flag to find those parent\nclasses and add them to the SpockBuilder *args (input classes)."),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  tuple of any lazily discovered classes"),(0,r.kt)("h4",{id:"_build-4"},"_","build"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _build() -> Dict\n")),(0,r.kt)("p",null,"Builds a dictionary of nodes and their edges (essentially builds the DAG)"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  dictionary of nodes and their edges"))}u.isMDXComponent=!0}}]);