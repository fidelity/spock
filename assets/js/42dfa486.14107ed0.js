"use strict";(self.webpackChunkdocs_v_2=self.webpackChunkdocs_v_2||[]).push([[6049],{3905:function(e,t,n){n.d(t,{Zo:function(){return s},kt:function(){return m}});var a=n(7294);function l(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function r(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function o(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?r(Object(n),!0).forEach((function(t){l(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):r(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function i(e,t){if(null==e)return{};var n,a,l=function(e,t){if(null==e)return{};var n,a,l={},r=Object.keys(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||(l[n]=e[n]);return l}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(l[n]=e[n])}return l}var p=a.createContext({}),u=function(e){var t=a.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):o(o({},t),e)),n},s=function(e){var t=u(e.components);return a.createElement(p.Provider,{value:t},e.children)},k={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},c=a.forwardRef((function(e,t){var n=e.components,l=e.mdxType,r=e.originalType,p=e.parentName,s=i(e,["components","mdxType","originalType","parentName"]),c=u(n),m=l,d=c["".concat(p,".").concat(m)]||c[m]||k[m]||r;return n?a.createElement(d,o(o({ref:t},s),{},{components:n})):a.createElement(d,o({ref:t},s))}));function m(e,t){var n=arguments,l=t&&t.mdxType;if("string"==typeof e||l){var r=n.length,o=new Array(r);o[0]=c;var i={};for(var p in t)hasOwnProperty.call(t,p)&&(i[p]=t[p]);i.originalType=e,i.mdxType="string"==typeof e?e:l,o[1]=i;for(var u=2;u<r;u++)o[u]=n[u];return a.createElement.apply(null,o)}return a.createElement.apply(null,n)}c.displayName="MDXCreateElement"},9352:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return i},contentTitle:function(){return p},metadata:function(){return u},toc:function(){return s},default:function(){return c}});var a=n(7462),l=n(3366),r=(n(7294),n(3905)),o=["components"],i={sidebar_label:"utils",title:"utils"},p=void 0,u={unversionedId:"reference/utils",id:"reference/utils",isDocsHomePage:!1,title:"utils",description:"Utility functions for Spock",source:"@site/docs/reference/utils.md",sourceDirName:"reference",slug:"/reference/utils",permalink:"/spock/reference/utils",editUrl:"https://github.com/fidelity/spock/edit/master/website/docs/reference/utils.md",tags:[],version:"current",frontMatter:{sidebar_label:"utils",title:"utils"},sidebar:"api",previous:{title:"handlers",permalink:"/spock/reference/handlers"}},s=[],k={toc:s};function c(e){var t=e.components,n=(0,l.Z)(e,o);return(0,r.kt)("wrapper",(0,a.Z)({},k,n,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("p",null,"Utility functions for Spock"),(0,r.kt)("h4",{id:"_filter_optional"},"_","filter","_","optional"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _filter_optional(val: List, allow_optional: bool = True)\n")),(0,r.kt)("p",null,"Filters an iterable for None values if they are allowed"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"val")," - iterable of values that might contain None"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"allow_optional")," - allows the check to succeed if a given val in the iterable is None")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  filtered list of values with None values removed"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Raises"),":"),(0,r.kt)("p",null,"  _SpockValueError"),(0,r.kt)("h4",{id:"sum_vals"},"sum","_","vals"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def sum_vals(val: List[Union[float, int, None]], sum_val: Union[float, int], allow_optional: bool = True, rel_tol: float = 1e-9, abs_tol: float = 0.0)\n")),(0,r.kt)("p",null,"Checks if an iterable of values sums within tolerance to a specified value"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"val")," - iterable of values to sum"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"sum_val")," - sum value to compare against"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"allow_optional")," - allows the check to succeed if a given val in the iterable is None"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"rel_tol")," - relative tolerance \u2013 it is the maximum allowed difference between a and b"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"abs_tol")," - the minimum absolute tolerance \u2013 useful for comparisons near zero")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  None"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Raises"),":"),(0,r.kt)("p",null,"  _SpockValueError"),(0,r.kt)("h4",{id:"eq_len"},"eq","_","len"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def eq_len(val: List[Union[Tuple, List, None]], allow_optional: bool = True)\n")),(0,r.kt)("p",null,"Checks that all values passed in the iterable are of the same length"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"val")," - iterable to compare lengths"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"allow_optional")," - allows the check to succeed if a given val in the iterable is None")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  None"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Raises"),":"),(0,r.kt)("p",null,"  _SpockValueError"),(0,r.kt)("h4",{id:"within"},"within"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def within(val: Union[float, int, None], low_bound: Union[float, int], upper_bound: Union[float, int], inclusive_lower: bool = False, inclusive_upper: bool = False, allow_optional: bool = True) -> None\n")),(0,r.kt)("p",null,"Checks that a value is within a defined range"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"val")," - value to check against"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"low_bound")," - lower bound of range"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"upper_bound")," - upper bound of range"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"inclusive_lower")," - if the check includes the bound value (i.e. ",">","=)"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"inclusive_upper")," - if the check includes the bound value (i.e. ","<","=)"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"allow_optional")," - allows the check to succeed if val is none")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  None"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Raises"),":"),(0,r.kt)("p",null,"  _SpockValueError"),(0,r.kt)("h4",{id:"ge"},"ge"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def ge(val: Union[float, int, None], bound: Union[float, int], allow_optional: bool = True) -> None\n")),(0,r.kt)("p",null,"Checks that a value is greater than or equal to (inclusive) a lower bound"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"val")," - value to check against"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"bound")," - lower bound"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"allow_optional")," - allows the check to succeed if val is none")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  None"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Raises"),":"),(0,r.kt)("p",null,"  _SpockValueError"),(0,r.kt)("h4",{id:"gt"},"gt"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def gt(val: Union[float, int, None], bound: Union[float, int], allow_optional: bool = True) -> None\n")),(0,r.kt)("p",null,"Checks that a value is greater (non-inclusive) than a lower bound"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"val")," - value to check against"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"bound")," - lower bound"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"allow_optional")," - allows the check to succeed if val is none")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  None"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Raises"),":"),(0,r.kt)("p",null,"  _SpockValueError"),(0,r.kt)("h4",{id:"le"},"le"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def le(val: Union[float, int, None], bound: Union[float, int], allow_optional: bool = True) -> None\n")),(0,r.kt)("p",null,"Checks that a value is less than or equal to (inclusive) an upper bound"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"val")," - value to check against"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"bound")," - upper bound"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"allow_optional")," - allows the check to succeed if val is none")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  None"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Raises"),":"),(0,r.kt)("p",null,"  _SpockValueError"),(0,r.kt)("h4",{id:"lt"},"lt"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def lt(val: Union[float, int], bound: Union[float, int], allow_optional: bool = True) -> None\n")),(0,r.kt)("p",null,"Checks that a value is less (non-inclusive) than an upper bound"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"val")," - value to check against"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"bound")," - upper bound"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"allow_optional")," - allows the check to succeed if val is none")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  None"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Raises"),":"),(0,r.kt)("p",null,"  _SpockValueError"),(0,r.kt)("h4",{id:"_find_all_spock_classes"},"_","find","_","all","_","spock","_","classes"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _find_all_spock_classes(attr_class: _C) -> List\n")),(0,r.kt)("p",null,"Within a spock class determine if there are any references to other spock classes"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"attr_class")," - a class with attrs attributes")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  list of dependent spock classes"),(0,r.kt)("h4",{id:"_check_4_spock_iterable"},"_","check","_","4","_","spock","_","iterable"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _check_4_spock_iterable(iter_obj: Union[Tuple, List]) -> bool\n")),(0,r.kt)("p",null,"Checks if an iterable type contains a spock class"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"iter_obj")," - iterable type")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  boolean if the iterable contains at least one spock class"),(0,r.kt)("h4",{id:"_get_enum_classes"},"_","get","_","enum","_","classes"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _get_enum_classes(enum_obj: EnumMeta) -> List\n")),(0,r.kt)("p",null,"Checks if any of the values of an enum are spock classes and adds to a list"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"enum_obj")," - enum class")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  list of enum values that are spock classes"),(0,r.kt)("h4",{id:"path_object_to_s3path"},"path","_","object","_","to","_","s3path"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def path_object_to_s3path(path: Path) -> str\n")),(0,r.kt)("p",null,"Convert a path object into a string s3 path"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"path")," - a spock config path")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  string of s3 path"),(0,r.kt)("h4",{id:"check_path_s3"},"check","_","path","_","s3"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def check_path_s3(path: Path) -> bool\n")),(0,r.kt)("p",null,"Checks the given path to see if it matches the s3:// regex"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"path")," - a spock config path")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  boolean of regex match"),(0,r.kt)("h4",{id:"_is_spock_instance"},"_","is","_","spock","_","instance"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _is_spock_instance(__obj: object) -> bool\n")),(0,r.kt)("p",null,"Checks if the object is a @spock decorated class"),(0,r.kt)("p",null,"Private interface that checks to see if the object passed in is registered within the spock module and also\nis a class with attrs attributes (",(0,r.kt)("strong",{parentName:"p"},"attrs_attrs"),")"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"__obj")," - class to inspect")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  bool"),(0,r.kt)("h4",{id:"_is_spock_tune_instance"},"_","is","_","spock","_","tune","_","instance"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _is_spock_tune_instance(__obj: object) -> bool\n")),(0,r.kt)("p",null,"Checks if the object is a @spock decorated class"),(0,r.kt)("p",null,"Private interface that checks to see if the object passed in is registered within the spock module tune addon and also\nis a class with attrs attributes (",(0,r.kt)("strong",{parentName:"p"},"attrs_attrs"),")"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"__obj")," - class to inspect")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  bool"),(0,r.kt)("h4",{id:"_check_iterable"},"_","check","_","iterable"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _check_iterable(iter_obj: Union[Tuple, List, EnumMeta]) -> bool\n")),(0,r.kt)("p",null,"Check if an iterable type contains a spock class"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"iter_obj")," - iterable type")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  boolean if the iterable contains at least one spock class"),(0,r.kt)("h4",{id:"make_argument"},"make","_","argument"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def make_argument(arg_name: str, arg_type: _T, parser: Type[_ArgumentGroup]) -> _ArgumentGroup\n")),(0,r.kt)("p",null,"Make argparser argument based on type"),(0,r.kt)("p",null,"Based on the type passed in handle the creation of the argparser argument so that overrides will have the correct\nbehavior when set"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"arg_name")," - name for the argument"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"arg_type")," - type of the argument"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"parser")," - current parser")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"parser")," - updated argparser")),(0,r.kt)("h4",{id:"_handle_generic_type_args"},"_","handle","_","generic","_","type","_","args"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def _handle_generic_type_args(val: str) -> Any\n")),(0,r.kt)("p",null,"Evaluates a string containing a Python literal"),(0,r.kt)("p",null,"Seeing a list and tuple types will come in as string literal format, use ast to get the actual type"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"val")," - string literal")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  the underlying string literal type"),(0,r.kt)("h4",{id:"add_info"},"add","_","info"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def add_info() -> Dict\n")),(0,r.kt)("p",null,"Adds extra information to the output dictionary"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"out_dict")," - output dictionary")),(0,r.kt)("h4",{id:"make_blank_git"},"make","_","blank","_","git"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def make_blank_git(out_dict: Dict) -> Dict\n")),(0,r.kt)("p",null,"Adds blank git info"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"out_dict")," - current output dictionary")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"out_dict")," - output dictionary with added git info")),(0,r.kt)("h4",{id:"add_repo_info"},"add","_","repo","_","info"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def add_repo_info(out_dict: Dict) -> Dict\n")),(0,r.kt)("p",null,"Adds GIT information to the output dictionary"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"out_dict")," - output dictionary")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"out_dict")," - output dictionary")),(0,r.kt)("h4",{id:"add_generic_info"},"add","_","generic","_","info"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def add_generic_info(out_dict: Dict) -> Dict\n")),(0,r.kt)("p",null,"Adds date, fqdn information to the output dictionary"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"out_dict")," - output dictionary")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"out_dict")," - output dictionary")),(0,r.kt)("h4",{id:"_maybe_docker"},"_","maybe","_","docker"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'def _maybe_docker(cgroup_path: str = "/proc/self/cgroup") -> bool\n')),(0,r.kt)("p",null,"Make a best effort to determine if run in a docker container"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"cgroup_path")," - path to cgroup file")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  boolean of best effort docker determination"),(0,r.kt)("h4",{id:"_maybe_k8s"},"_","maybe","_","k8s"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'def _maybe_k8s(cgroup_path: str = "/proc/self/cgroup") -> bool\n')),(0,r.kt)("p",null,"Make a best effort to determine if run in a container via k8s"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"cgroup_path")," - path to cgroup file")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("p",null,"  boolean of best effort k8s determination"),(0,r.kt)("h4",{id:"deep_payload_update"},"deep","_","payload","_","update"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"def deep_payload_update(source: Dict, updates: Dict) -> Dict\n")),(0,r.kt)("p",null,"Deeply updates a dictionary"),(0,r.kt)("p",null,"Iterates through a dictionary recursively to update individual values within a possibly nested dictionary\nof dictionaries -- creates a dictionary if empty and trying to recurse"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"source")," - source dictionary"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"updates")," - updates to the dictionary")),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Returns"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"source")," - updated version of the source dictionary")),(0,r.kt)("h4",{id:"check_payload_overwrite"},"check","_","payload","_","overwrite"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'def check_payload_overwrite(payload: Dict, updates: Dict, configs: str, overwrite: str = "") -> None\n')),(0,r.kt)("p",null,"Warns when parameters are overwritten across payloads as order will matter"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"payload")," - current payload"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"payload_update")," - update to add to payload"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"configs")," - config path"),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"overwrite")," - name of parent")))}c.isMDXComponent=!0}}]);