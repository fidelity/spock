"use strict";(self.webpackChunkdocs_v_2=self.webpackChunkdocs_v_2||[]).push([[5988],{3905:function(e,t,n){n.d(t,{Zo:function(){return c},kt:function(){return m}});var a=n(7294);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},o=Object.keys(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var p=a.createContext({}),l=function(e){var t=a.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},c=function(e){var t=l(e.components);return a.createElement(p.Provider,{value:t},e.children)},u={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},d=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,o=e.originalType,p=e.parentName,c=s(e,["components","mdxType","originalType","parentName"]),d=l(n),m=r,h=d["".concat(p,".").concat(m)]||d[m]||u[m]||o;return n?a.createElement(h,i(i({ref:t},c),{},{components:n})):a.createElement(h,i({ref:t},c))}));function m(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var o=n.length,i=new Array(o);i[0]=d;var s={};for(var p in t)hasOwnProperty.call(t,p)&&(s[p]=t[p]);s.originalType=e,s.mdxType="string"==typeof e?e:r,i[1]=s;for(var l=2;l<o;l++)i[l]=n[l];return a.createElement.apply(null,i)}return a.createElement.apply(null,n)}d.displayName="MDXCreateElement"},1093:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return s},contentTitle:function(){return p},metadata:function(){return l},toc:function(){return c},default:function(){return d}});var a=n(7462),r=n(3366),o=(n(7294),n(3905)),i=["components"],s={},p="Optuna Support",l={unversionedId:"addons/tuner/Optuna",id:"addons/tuner/Optuna",isDocsHomePage:!1,title:"Optuna Support",description:"spock integrates with the Optuna hyper-parameter optimization framework through the provided",source:"@site/docs/addons/tuner/Optuna.md",sourceDirName:"addons/tuner",slug:"/addons/tuner/Optuna",permalink:"/spock/addons/tuner/Optuna",editUrl:"https://github.com/fidelity/spock/edit/master/website/docs/addons/tuner/Optuna.md",tags:[],version:"current",frontMatter:{},sidebar:"docs",previous:{title:"Ax Support",permalink:"/spock/addons/tuner/Ax"},next:{title:"Saving Hyper-Parameter Configs -- Base, Samples, and Best",permalink:"/spock/addons/tuner/Saving"}},c=[{value:"Defining the Backend",id:"defining-the-backend",children:[]},{value:"Generate Functionality Still Exists",id:"generate-functionality-still-exists",children:[]},{value:"Sample as an Alternative to Generate",id:"sample-as-an-alternative-to-generate",children:[]}],u={toc:c};function d(e){var t=e.components,n=(0,r.Z)(e,i);return(0,o.kt)("wrapper",(0,a.Z)({},u,n,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"optuna-support"},"Optuna Support"),(0,o.kt)("p",null,(0,o.kt)("inlineCode",{parentName:"p"},"spock")," integrates with the Optuna hyper-parameter optimization framework through the provided\nask-and-run interface and the define-and-run API. See ",(0,o.kt)("a",{parentName:"p",href:"https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/009_ask_and_tell.html#define-and-run"},"docs"),"."),(0,o.kt)("p",null,"All examples can be found ",(0,o.kt)("a",{parentName:"p",href:"https://github.com/fidelity/spock/blob/master/examples"},"here"),"."),(0,o.kt)("h3",{id:"defining-the-backend"},"Defining the Backend"),(0,o.kt)("p",null,"So let's continue in our Optuna specific version of ",(0,o.kt)("inlineCode",{parentName:"p"},"tune.py"),":"),(0,o.kt)("p",null,"It's important to note that you can still use the ",(0,o.kt)("inlineCode",{parentName:"p"},"@spock")," decorator to define any non hyper-parameters! For\nposterity let's add some fixed parameters (those that are not part of hyper-parameter tuning) that we will use\nelsewhere in our code. "),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"from spock import spock\n\nfrom spock.addons.tune import (\n    ChoiceHyperParameter,\n    RangeHyperParameter,\n    spockTuner,\n)\n\n@spock\nclass BasicParams:\n    n_trials: int\n    max_iter: int\n\n\n@spockTuner\nclass LogisticRegressionHP:\n    c: RangeHyperParameter\n    solver: ChoiceHyperParameter\n")),(0,o.kt)("p",null,"Now we need to tell ",(0,o.kt)("inlineCode",{parentName:"p"},"spock")," that we intend on doing hyper-parameter tuning and which backend we would like to use. We\ndo this by calling the ",(0,o.kt)("inlineCode",{parentName:"p"},"tuner")," method on the ",(0,o.kt)("inlineCode",{parentName:"p"},"SpockBuilder")," object passing in a configuration object for the\nbackend of choice (just like in basic functionality this is a chained command, thus the builder object will still be\nreturned). For Optuna one uses ",(0,o.kt)("inlineCode",{parentName:"p"},"OptunaTunerConfig"),". This config mirrors all options that would be passed into\nthe ",(0,o.kt)("inlineCode",{parentName:"p"},"optuna.study.create_study")," function call so that ",(0,o.kt)("inlineCode",{parentName:"p"},"spock")," can setup the define-and-run API. (Note: The ",(0,o.kt)("inlineCode",{parentName:"p"},"@spockTuner"),"\ndecorated classes are passed to the ",(0,o.kt)("inlineCode",{parentName:"p"},"SpockBuilder")," in the exact same way as basic ",(0,o.kt)("inlineCode",{parentName:"p"},"@spock"),"\ndecorated classes.)"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},'from spock import SpockBuilder\nfrom spock.addons.tune import OptunaTunerConfig\n\n# Optuna config -- this will internally configure the study object for the define-and-run style which will be returned\n# by accessing the tuner_status property on the SpockBuilder object\noptuna_config = OptunaTunerConfig(\n    study_name="Iris Logistic Regression", direction="maximize"\n)\n\n# Use the builder to setup\n# Call tuner to indicate that we are going to do some HP tuning -- passing in an optuna study object\nattrs_obj = SpockBuilder(\n    LogisticRegressionHP,\n    BasicParams,\n    desc="Example Logistic Regression Hyper-Parameter Tuning -- Optuna Backend",\n).tuner(tuner_config=optuna_config)\n\n')),(0,o.kt)("h3",{id:"generate-functionality-still-exists"},"Generate Functionality Still Exists"),(0,o.kt)("p",null,"To get the set of fixed parameters (those that are not hyper-parameters) one simply calls the ",(0,o.kt)("inlineCode",{parentName:"p"},"generate()")," function\njust like they would for normal ",(0,o.kt)("inlineCode",{parentName:"p"},"spock")," usage to get the fixed parameter ",(0,o.kt)("inlineCode",{parentName:"p"},"spockspace"),". "),(0,o.kt)("p",null,"Continuing in ",(0,o.kt)("inlineCode",{parentName:"p"},"tune.py"),":"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"\n# Here we need some of the fixed parameters first so we can just call the generate fnc to grab all the fixed params\n# prior to starting the sampling process\nfixed_params = attrs_obj.generate()\n")),(0,o.kt)("h3",{id:"sample-as-an-alternative-to-generate"},"Sample as an Alternative to Generate"),(0,o.kt)("p",null,"The ",(0,o.kt)("inlineCode",{parentName:"p"},"sample()")," call is the crux of ",(0,o.kt)("inlineCode",{parentName:"p"},"spock")," hyper-parameter tuning support. It draws a hyper-parameter sample from the\nunderlying backend sampler and combines it with fixed parameters and returns a single ",(0,o.kt)("inlineCode",{parentName:"p"},"Spockspace")," with all\nuseable parameters (defined with dot notation). For Optuna -- Under the hood ",(0,o.kt)("inlineCode",{parentName:"p"},"spock")," uses the define-and-run Optuna\ninterface -- thus it handles the underlying 'ask' call. The ",(0,o.kt)("inlineCode",{parentName:"p"},"spock")," builder object has a ",(0,o.kt)("inlineCode",{parentName:"p"},"@property")," called\n",(0,o.kt)("inlineCode",{parentName:"p"},"tuner_status")," that returns any necessary backend objects in a dictionary that the user needs to interface with. In the\ncase of Optuna, this contains both the Optuna ",(0,o.kt)("inlineCode",{parentName:"p"},"study")," and ",(0,o.kt)("inlineCode",{parentName:"p"},"trial")," (as dictionary keys). We use the return of\n",(0,o.kt)("inlineCode",{parentName:"p"},"tuner_status")," to handle the 'tell' call based on the metric of interested (here just simple validation accuracy)"),(0,o.kt)("p",null,"Continuing in ",(0,o.kt)("inlineCode",{parentName:"p"},"tune.py"),":"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},'# Iterate through a bunch of optuna trials\nfor _ in range(fixed_params.BasicParams.n_trials):\n        # Call sample on the spock object \n        hp_attrs = attrs_obj.sample()\n        # Use the currently sampled parameters in a simple LogisticRegression from sklearn\n        clf = LogisticRegression(\n            C=hp_attrs.LogisticRegressionHP.c,\n            solver=hp_attrs.LogisticRegressionHP.solver,\n            max_iter=hp_attrs.BasicParams.max_iter\n        )\n        clf.fit(X_train, y_train)\n        val_acc = clf.score(X_valid, y_valid)\n        # Get the status of the tuner -- this dict will contain all the objects needed to update\n        tuner_status = attrs_obj.tuner_status\n        # Pull the study and trials object out of the return dictionary and pass it to the tell call using the study\n        # object\n        tuner_status["study"].tell(tuner_status["trial"], val_acc)\n')))}d.isMDXComponent=!0}}]);