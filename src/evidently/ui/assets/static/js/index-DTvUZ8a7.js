const __vite__fileDeps=["static/js/index-DxEA__Um.js","static/js/vendor-C2GWNUp2.js","static/js/index-EteN2ABT.js","static/js/DashboardViewParams-D9XhJzJS.js","static/js/DashboardWidgets-16CRiwfE.js","static/js/DashboardContent-Dds924lH.js","static/js/index-DDgANbm4.js","static/js/index-LT2YNxwo.js","static/js/index-qb_niS19.js","static/js/index-DJhIIsZf.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
var se=Object.defineProperty;var oe=(e,t,s)=>t in e?se(e,t,{enumerable:!0,configurable:!0,writable:!0,value:s}):e[t]=s;var I=(e,t,s)=>(oe(e,typeof t!="symbol"?t+"":t,s),s);import{c as U,g as R,u as ne,a as ie,r as k,j as r,A as ae,b as ce,d as F,i as he,T as g,e as le,R as M,S as W,B as d,I as J,C as q,f as de,h as ue,k as pe,l as me,m as E,n as fe,L as je,o as xe,p as Le,q as ye,P as ge,s as _e,t as ve,v as Ce,w as Se,G as w,F as Ee,x as be,y as ke,z as Ie,D as we,M as m,E as H,H as Pe,J as Te,K as A,N as p,O as Oe,Q as Ae,U as De,V as Re,W as Me}from"./vendor-C2GWNUp2.js";(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const n of document.querySelectorAll('link[rel="modulepreload"]'))o(n);new MutationObserver(n=>{for(const i of n)if(i.type==="childList")for(const a of i.addedNodes)a.tagName==="LINK"&&a.rel==="modulepreload"&&o(a)}).observe(document,{childList:!0,subtree:!0});function s(n){const i={};return n.integrity&&(i.integrity=n.integrity),n.referrerPolicy&&(i.referrerPolicy=n.referrerPolicy),n.crossOrigin==="use-credentials"?i.credentials="include":n.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function o(n){if(n.ep)return;n.ep=!0;const i=s(n);fetch(n.href,i)}})();const{transitions:b}=U(),P="#ed0500",Fe=U({cssVariables:{colorSchemeSelector:"class"},colorSchemes:{light:{palette:{text:{primary:"#09090b"},primary:{main:"#09090b",light:R[200]},secondary:{main:P,dark:"#c10400",light:R[200]}}},dark:{palette:{text:{primary:"#fafafa"},primary:{main:"#fafafa",light:R[900]},secondary:{main:P}}}},shape:{borderRadius:5},components:{MuiInputBase:{styleOverrides:{input:{"&:-webkit-autofill":{transitionDelay:"9999s",transitionProperty:"background-color, box-shadow, color"}}}},MuiLink:{styleOverrides:{root:{transition:b.create("color",{duration:b.duration.enteringScreen}),"&:hover":{color:P}}}},MuiTabs:{styleOverrides:{flexContainer:{gap:"10px"},indicator:{backgroundColor:P}}},MuiTab:{defaultProps:{color:"secondary"},styleOverrides:{root:{fontSize:"1rem",borderRadius:"5px"}}},MuiIconButton:{styleOverrides:{root:{transition:b.create("color",{duration:b.duration.enteringScreen}),color:"inherit","&:hover":{color:P}}}},MuiSwitch:{defaultProps:{color:"secondary"}},MuiToggleButton:{defaultProps:{color:"secondary"},styleOverrides:{root:{transition:b.create("color",{duration:b.duration.enteringScreen}),color:"inherit","&.Mui-disabled":{border:"unset"}}}},MuiLinearProgress:{defaultProps:{color:"secondary"}},MuiPaper:{defaultProps:{sx:{border:"1px solid",borderColor:e=>e.palette.divider}},styleOverrides:{root:{boxShadow:"unset"}}}},typography:{fontFamily:["-apple-system","BlinkMacSystemFont",'"Segoe UI"',"Roboto",'"Helvetica Neue"',"Arial","sans-serif",'"Apple Color Emoji"','"Segoe UI Emoji"','"Segoe UI Symbol"'].join(","),button:{fontWeight:"bold",textTransform:"none"}}}),Q=()=>{const{mode:e}=ne(),t=ie("(prefers-color-scheme: dark)");return!e||e==="system"?t?"dark":"light":e},wt=()=>{const e=Q();return k.useMemo(()=>e==="dark"?{tooltip:{container:{background:"#000",color:"#fff"}}}:void 0,[e])},N=({forseFilled:e,sx:t,...s})=>{const o=Q();return r.jsx(ae,{sx:[n=>n.applyStyles("light",{border:"none"}),...Array.isArray(t)?t:[t]],variant:o==="dark"?e?"filled":"outlined":void 0,...s})},v=()=>{var t;const e=ce();return r.jsxs(N,{severity:"error",children:[r.jsx(F,{children:"Something went wrong"}),he(e)&&r.jsxs(r.Fragment,{children:[r.jsx(g,{fontWeight:"bold",children:[`Status: ${e.status}`,typeof((t=e.data)==null?void 0:t.detail)=="string"&&e.data.detail].filter(Boolean).join(", ")}),typeof e.data=="string"&&r.jsx(g,{children:e.data})]}),typeof e=="string"&&r.jsx(g,{fontWeight:"bold",children:e})]})},Y=({data:e})=>{const[t,s]=M.useState(!1),o=M.useRef(null);return k.useEffect(()=>{e!=null&&e.error&&(o.current=e.error,s(!0))},[e]),r.jsx(W,{open:t,onClose:(n,i)=>{i!=="clickaway"&&s(!1)},children:r.jsx(d,{children:r.jsx(N,{severity:"error",forseFilled:!0,children:r.jsxs(d,{display:"flex",justifyContent:"space-between",alignItems:"flex-start",gap:2,children:[r.jsxs(d,{children:[r.jsx(F,{children:"Something went wrong"}),o.current&&r.jsx(g,{fontWeight:"bold",children:[typeof o.current.status_code=="number"&&`Status: ${o.current.status_code}`,typeof o.current.detail=="string"&&o.current.detail].filter(Boolean).join(", ")})]}),r.jsx(d,{children:r.jsx(J,{size:"small","aria-label":"close",color:"inherit",onClick:()=>{s(!1)},children:r.jsx(q,{})})})]})})})})},B=()=>{const e=le();return r.jsx(Y,{data:e})},Ne=()=>{var s;const t=(s=de().find(o=>{var n;return!!((n=o.data)!=null&&n.error)}))==null?void 0:s.data;return r.jsx(Y,{data:t})},Be={path:"*",Component:()=>r.jsx(d,{display:"flex",justifyContent:"center",children:r.jsx(g,{variant:"h4",children:"Page Not Found"})})},$e="modulepreload",He=function(e){return"/"+e},V={},_=function(t,s,o){let n=Promise.resolve();if(s&&s.length>0){document.getElementsByTagName("link");const i=document.querySelector("meta[property=csp-nonce]"),a=(i==null?void 0:i.nonce)||(i==null?void 0:i.getAttribute("nonce"));n=Promise.all(s.map(c=>{if(c=He(c),c in V)return;V[c]=!0;const f=c.endsWith(".css"),h=f?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${c}"]${h}`))return;const l=document.createElement("link");if(l.rel=f?"stylesheet":$e,f||(l.as="script",l.crossOrigin=""),l.href=c,a&&l.setAttribute("nonce",a),document.head.appendChild(l),f)return new Promise((x,D)=>{l.addEventListener("load",x),l.addEventListener("error",()=>D(new Error(`Unable to preload CSS for ${c}`)))})}))}return n.then(()=>t()).catch(i=>{const a=new Event("vite:preloadError",{cancelable:!0});if(a.payload=i,window.dispatchEvent(a),!a.defaultPrevented)throw i})},Ve=()=>r.jsx(ue,{fontSize:"large",sx:{width:180},children:r.jsxs("svg",{"aria-hidden":"true",width:"734",height:"219",viewBox:"0 70 734 90",version:"1.1",children:[r.jsx("path",{d:"M 180 113 L 180 141 201.500 141 L 223 141 223 136.500 L 223 132 207 132 L 191 132 191 124.500 L 191 117 204.500 117 L 218 117 218 112.500 L 218 108 204.500 108 L 191 108 191 101 L 191 94 206 94 L 221 94 221 89.500 L 221 85 200.500 85 L 180 85 180 113 M 221.989 87.250 C 221.983 88.487, 227.010 101.088, 233.160 115.250 L 244.342 141 249.931 141 L 255.521 141 266.865 114.959 C 273.104 100.636, 278.439 88.036, 278.721 86.959 C 279.183 85.191, 278.709 85.002, 273.867 85.024 L 268.500 85.049 259.393 106.080 L 250.285 127.111 243.204 110.806 C 239.309 101.838, 235.210 92.362, 234.096 89.750 L 232.071 85 227.036 85 C 222.483 85, 221.999 85.216, 221.989 87.250 M 280 113 L 280 141 285.500 141 L 291 141 291 113 L 291 85 285.500 85 L 280 85 280 113 M 301 113 L 301 141 316.818 141 C 327.946 141, 334.130 140.557, 337.672 139.505 C 340.601 138.635, 344.617 136.329, 347.270 133.993 C 349.779 131.785, 352.871 127.845, 354.141 125.239 C 355.926 121.575, 356.450 118.799, 356.450 113 C 356.450 107.201, 355.926 104.425, 354.141 100.761 C 352.871 98.155, 349.779 94.215, 347.270 92.007 C 344.617 89.671, 340.601 87.365, 337.672 86.495 C 334.130 85.443, 327.946 85, 316.818 85 L 301 85 301 113 M 362 113 L 362 141 383.500 141 L 405 141 405 136.500 L 405 132 389 132 L 373 132 373 124.500 L 373 117 386.500 117 L 400 117 400 112.500 L 400 108 386.500 108 L 373 108 373 101 L 373 94 388.500 94 L 404 94 404 89.500 L 404 85 383 85 L 362 85 362 113 M 411 113 L 411 141 416.500 141 L 422 141 422 122.426 L 422 103.851 437.126 122.426 L 452.253 141 457.126 141 L 462 141 462 113 L 462 85 456.522 85 L 451.044 85 450.772 103.414 L 450.500 121.828 435.550 103.414 L 420.600 85 415.800 85 L 411 85 411 113 M 464 89.500 L 464 94 473.500 94 L 483 94 483 117.500 L 483 141 488.500 141 L 494 141 494 117.500 L 494 94 503 94 L 512 94 512 89.500 L 512 85 488 85 L 464 85 464 89.500 M 514 113 L 514 141 534.500 141 L 555 141 555 136.500 L 555 132 540.500 132 L 526 132 526 108.500 L 526 85 520 85 L 514 85 514 113 M 544 85.624 C 544 85.967, 548.725 94.001, 554.500 103.477 L 565 120.707 565 130.853 L 565 141 571 141 L 577 141 577 130.825 L 577 120.649 587.500 103.291 C 593.275 93.743, 598 85.722, 598 85.466 C 598 85.210, 595.577 85, 592.615 85 L 587.230 85 579.505 97.991 C 575.257 105.136, 571.435 110.769, 571.012 110.507 C 570.589 110.246, 566.926 104.410, 562.872 97.538 L 555.500 85.043 549.750 85.021 C 546.587 85.010, 544 85.281, 544 85.624 M 312 113 L 312 132 320.250 131.994 C 324.788 131.991, 330.174 131.524, 332.219 130.956 C 334.264 130.388, 337.363 128.724, 339.105 127.258 C 340.847 125.793, 342.886 123.124, 343.636 121.329 C 344.386 119.533, 345 115.785, 345 113 C 345 110.215, 344.386 106.467, 343.636 104.671 C 342.886 102.876, 340.847 100.207, 339.105 98.742 C 337.363 97.276, 334.264 95.612, 332.219 95.044 C 330.174 94.476, 324.788 94.009, 320.250 94.006 L 312 94 312 113",fill:"currentColor",fillRule:"evenodd"}),r.jsx("path",{d:"M 121 112 L 121 169 133.500 169 L 146 169 146 112 L 146 55 133.500 55 L 121 55 121 112 M 77 126 L 77 169 90 169 L 103 169 103 126 L 103 83 90 83 L 77 83 77 126 M 633.540 88.199 C 632.771 90.015, 627.159 102.517, 621.070 115.982 C 614.982 129.447, 610 140.832, 610 141.282 C 610 141.732, 612.528 141.965, 615.617 141.800 L 621.235 141.500 623.794 135.250 L 626.353 129 640.218 129 L 654.084 129 657 135.500 L 659.916 142 665.526 142 C 670.413 142, 671.063 141.775, 670.577 140.250 C 670.271 139.287, 664.639 126.575, 658.064 112 L 646.108 85.500 640.524 85.199 C 635.051 84.904, 634.913 84.964, 633.540 88.199 M 673 113.500 L 673 142 678.500 142 L 684 142 684 113.500 L 684 85 678.500 85 L 673 85 673 113.500 M 635.630 107.723 C 633.074 113.650, 630.986 118.838, 630.991 119.250 C 630.996 119.662, 635.275 120, 640.500 120 C 645.725 120, 650 119.819, 650 119.598 C 650 119.377, 647.923 114.315, 645.385 108.348 C 642.847 102.382, 640.659 97.375, 640.524 97.223 C 640.389 97.070, 638.187 101.795, 635.630 107.723 M 34 140.500 L 34 169 47 169 L 60 169 60 140.500 L 60 112 47 112 L 34 112 34 140.500",fill:"#ed0500",fillRule:"evenodd"})]})});function u(e){return e!=null&&e.notThrowExc?Ge:ze}const ze=e=>{const{data:t,error:s,response:o}=e;if(s)throw pe(s,{status:o.status});return t},Ge=e=>{const{data:t,error:s,response:o}=e;return s?{error:{...s,status_code:o.status}}:t},Ue=({api:e})=>({loader:()=>e.GET("/api/version").then(u())}),We=me,C=We({baseUrl:"/"}),{loader:Je}=Ue({api:C}),qe={path:"/",lazy:async()=>{const{HomeComponentTemplate:e,...t}=await _(()=>import("./index-DxEA__Um.js"),__vite__mapDeps([0,1]));return{Component:()=>r.jsxs(r.Fragment,{children:[r.jsx(Ne,{}),r.jsx(e,{LogoSvg:Ve})]}),...t}},loader:Je,ErrorBoundary:v},K=e=>{if(e.id)return{...e,id:e.id};throw`"id" is missing in object: ${JSON.stringify(e)}`},X=e=>{if(e.headers.get("Content-type")!=="application/json")throw new Response("Unsupported Media Type",{status:415})},Qe=({api:e})=>({loader:({params:t})=>{const{projectId:s}=t;return E(s),e.GET("/api/projects/{project_id}/info",{params:{path:{project_id:s}}}).then(u()).then(K)}}),Ye=({event:e})=>{const t=e.points[0],s=t.customdata,o=t.x&&typeof t.x=="string"?t.x:null;if(!s)return r.jsx(r.Fragment,{});const n="metric_fingerprint"in s?"report":"test-suite";return r.jsx(r.Fragment,{children:r.jsx(d,{sx:{position:"absolute",bottom:0,right:0,background:i=>i.palette.background.default,p:1,borderRadius:"10px"},children:r.jsxs(fe,{direction:"row",alignItems:"center",gap:2,children:[o&&r.jsxs(g,{variant:"button",children:["Selected point timestamp: ",o]}),r.jsx(je,{component:xe,to:`${n}s/${s.snapshot_id}`,children:r.jsxs(Le,{variant:"outlined",children:["Go to ",n]})})]})})})},Ke=()=>{const[e,t]=ye("is-user-saw-click-on-datapoints-hint",!1),[s,o]=k.useState(!e);return k.useEffect(()=>t(!0),[]),s?r.jsx(r.Fragment,{children:r.jsx(W,{open:s,onClose:(n,i)=>{i!=="clickaway"&&o(!1)},children:r.jsx(ge,{sx:{p:1,borderRadius:2,border:"1px solid",borderColor:n=>n.palette.divider},children:r.jsxs(d,{display:"flex",justifyContent:"space-between",alignItems:"center",gap:2,children:[r.jsx(d,{children:r.jsx(g,{children:"Click on point in order to go to snapshot"})}),r.jsx(d,{children:r.jsx(J,{size:"small",onClick:()=>{o(!1)},children:r.jsx(q,{})})})]})})})}):r.jsx(r.Fragment,{})};function z(e){return`${e.getFullYear()}-${(e.getMonth()+1).toString().padStart(2,"0")}-${e.getDate().toString().padStart(2,"0")}T${e.getHours().toString().padStart(2,"0")}:${e.getMinutes().toString().padStart(2,"0")}`}const y={FROM:"date_from",TO:"date_to"},Xe=e=>{const t=e.get(y.FROM),s=e.get(y.TO);return{date_from:t,date_to:s}},Ze=({dataRanges:e})=>{const[t,s]=Te(),{date_from:o,date_to:n}=Xe(t),i=A(o||e.minDate),a=A(n||e.maxDate);return{isCorrectTimeInterval:i.isValid()&&a.isValid()&&(i.isSame(a)||i.isBefore(a)),date_from:i,date_to:a,setSearchParams:s}},Pt=({dataRanges:e,isDashboardHideDates:t,setIsDashboardHideDates:s,isShowDateFilter:o})=>{const n=_e(),{isCorrectTimeInterval:i,date_from:a,date_to:c,setSearchParams:f}=Ze({dataRanges:e}),[h,l]=k.useState({date_from:a,date_to:c}),x=ve(h,300),D=i?"":"incorrect time interval";return k.useEffect(()=>{var T,O;if(n)return;const j=(T=x==null?void 0:x.date_to)==null?void 0:T.toDate(),L=(O=x==null?void 0:x.date_from)==null?void 0:O.toDate();f(S=>(S.delete(y.FROM),S.delete(y.TO),L&&S.append(y.FROM,z(L)),j&&S.append(y.TO,z(j)),S),{preventScrollReset:!0,replace:!0})},[x]),r.jsx(Ce,{dateAdapter:Se,adapterLocale:"en-gb",children:r.jsxs(w,{container:!0,padding:1,zIndex:1,gap:2,justifyContent:"flex-end",alignItems:"flex-end",children:[r.jsx(w,{item:!0,children:r.jsx(d,{minWidth:180,display:"flex",justifyContent:"center",children:r.jsx(Ee,{control:r.jsx(be,{checked:t,onChange:j=>s(j.target.checked)}),label:"Show in order"})})}),o&&r.jsxs(r.Fragment,{children:[r.jsx(w,{item:!0,xs:12,md:2,children:r.jsxs(ke,{fullWidth:!0,children:[r.jsx(Ie,{children:"Period"}),r.jsxs(we,{variant:"standard",defaultValue:"",onChange:j=>{const[L,T]=j.target.value.split(",");if(L===""){l({date_from:null,date_to:null});return}const[O,S]=[Number(L),T],$=e.maxDate.subtract(O,S);l({date_from:$.isBefore(e.minDate)?e.minDate:$,date_to:e.maxDate})},children:[r.jsx(m,{value:"",children:r.jsx("em",{children:"None"})}),r.jsx(m,{value:"10,minutes",children:"Last 10 Minutes"}),r.jsx(m,{value:"30,minutes",children:"Last 30 Minutes"}),r.jsx(m,{value:"1,hours",children:"Last 1 Hours"}),r.jsx(m,{value:"2,hours",children:"Last 2 Hours"}),r.jsx(m,{value:"8,hours",children:"Last 8 Hours"}),r.jsx(m,{value:"24,hours",children:"Last 24 Hours"}),r.jsx(m,{value:"7,days",children:"Last 7 Days"}),r.jsx(m,{value:"14,days",children:"Last 14 Days"}),r.jsx(m,{value:"28,days",children:"Last 28 Days"}),r.jsx(m,{value:"60,days",children:"Last 60 Days"})]})]})}),r.jsx(w,{item:!0,children:r.jsxs(d,{display:"flex",alignItems:"center",gap:2,children:[r.jsx(H,{minDate:e.minDate,maxDate:e.maxDate&&c,slotProps:{textField:{variant:"standard"}},label:"From",value:h.date_from,onChange:j=>l(L=>({...L,date_from:j}))}),r.jsx(d,{height:1,display:"flex",alignItems:"center",children:r.jsx(g,{children:" - "})}),r.jsx(H,{minDate:e.minDate&&a,maxDate:e.maxDate,slotProps:{textField:{variant:"standard"}},label:"To",value:h.date_to,onChange:j=>l(L=>({...L,date_to:j}))})]})}),r.jsx(w,{item:!0,xs:12,children:r.jsx(Pe,{unmountOnExit:!0,in:!i,children:r.jsxs(N,{severity:"error",children:[r.jsx(F,{children:"Error"}),D]})})})]})]})})};class et{constructor(){I(this,"at",0);I(this,"ch","");I(this,"text","");I(this,"escapee",{'"':'"',"\\":"\\","/":"/",b:"\b",f:"\f",n:`
`,r:"\r",t:"	"})}error(t){throw{name:"SyntaxError",message:t,at:this.at,text:this.text}}next(){return this.ch=this.text.charAt(this.at++)}check(t){t!==this.ch&&this.error(`Expected '${t}' instead of '${this.ch}'`),this.ch=this.text.charAt(this.at++)}number(){var t="";if(this.ch==="-"&&(t="-",this.check("-")),this.ch==="I")return this.check("I"),this.check("n"),this.check("f"),this.check("i"),this.check("n"),this.check("i"),this.check("t"),this.check("y"),Number.NEGATIVE_INFINITY;for(;this.ch>="0"&&this.ch<="9";)t+=this.ch,this.next();if(this.ch===".")for(t+=".";this.next()&&this.ch>="0"&&this.ch<="9";)t+=this.ch;if(this.ch==="e"||this.ch==="E")for(t+=this.ch,this.next(),(this.ch==="-"||this.ch==="+")&&(t+=this.ch,this.next());this.ch>="0"&&this.ch<="9";)t+=this.ch,this.next();return+t}string(){var t,s,o="",n;if(this.ch==='"')for(;this.next();){if(this.ch==='"')return this.next(),o;if(this.ch==="\\")if(this.next(),this.ch==="u"){for(n=0,s=0;s<4&&(t=Number.parseInt(this.next(),16),!!isFinite(t));s++)n=n*16+t;o+=String.fromCharCode(n)}else if(this.escapee[this.ch])o+=this.escapee[this.ch];else break;else o+=this.ch}this.error("Bad string")}white(){for(;this.ch&&this.ch<=" ";)this.next()}word(){switch(this.ch){case"t":return this.check("t"),this.check("r"),this.check("u"),this.check("e"),!0;case"f":return this.check("f"),this.check("a"),this.check("l"),this.check("s"),this.check("e"),!1;case"n":return this.check("n"),this.check("u"),this.check("l"),this.check("l"),null;case"N":return this.check("N"),this.check("a"),this.check("N"),Number.NaN;case"I":return this.check("I"),this.check("n"),this.check("f"),this.check("i"),this.check("n"),this.check("i"),this.check("t"),this.check("y"),Number.POSITIVE_INFINITY}this.error("Unexpected '"+this.ch+"'")}array(){var t=[];if(this.ch==="["){if(this.check("["),this.white(),this.ch==="]")return this.check("]"),t;for(;this.ch;){if(t.push(this.value()),this.white(),this.ch==="]")return this.check("]"),t;this.check(","),this.white()}}this.error("Bad array")}object(){var t,s={};if(this.ch==="{"){if(this.check("{"),this.white(),this.ch==="}")return this.check("}"),s;for(;this.ch;){if(t=this.string(),this.white(),this.check(":"),Object.hasOwnProperty.call(s,t)&&this.error('Duplicate key "'+t+'"'),s[t]=this.value(),this.white(),this.ch==="}")return this.check("}"),s;this.check(","),this.white()}}this.error("Bad object")}value(){switch(this.white(),this.ch){case"{":return this.object();case"[":return this.array();case'"':return this.string();case"-":return this.number();default:return this.ch>="0"&&this.ch<="9"?this.number():this.word()}}parse(t,s){let o;return this.text=t,this.at=0,this.ch=" ",o=this.value(),this.white(),this.ch&&this.error("Syntax error"),s!==void 0?function n(i,a){var c,f,h=i[a];if(h&&typeof h=="object")for(c in h)Object.prototype.hasOwnProperty.call(h,c)&&(f=n(h,c),f!==void 0?h[c]=f:delete h[c]);return s.call(i,a,h)}({"":o},""):o}}const Z=e=>new et().parse(e),tt=({api:e})=>({loader:({params:t,request:s})=>{E(t.projectId);const{searchParams:o}=new URL(s.url);let n=o.get(y.FROM),i=o.get(y.TO);return n&&!A(n).isValid()&&(n=null),i&&!A(i).isValid()&&(i=null),e.GET("/api/projects/{project_id}/dashboard",{params:{path:{project_id:t.projectId},query:{timestamp_start:n,timestamp_end:i}},parseAs:"text"}).then(u()).then(Z)}}),{loader:rt}=tt({api:C}),st={index:!0,id:"dashboard",lazy:async()=>{const[{DashboardComponentTemplate:e},{DashboardWidgets:t}]=await Promise.all([_(()=>import("./index-EteN2ABT.js"),__vite__mapDeps([2,1,3])),_(()=>import("./DashboardWidgets-16CRiwfE.js"),__vite__mapDeps([4,1,5,3]))]);return{Component:()=>r.jsx(e,{Dashboard:({data:{widgets:s}})=>r.jsx(t,{widgets:s}),OnClickedPointComponent:Ye,OnHoveredPlotComponent:Ke})}},loader:rt,ErrorBoundary:v},ee={RELOAD_SNAPSHOTS:"reload-snapshots",DELETE_SNAPSHOT:"delete-snapshot"},ot=p.object({action:p.literal(ee.RELOAD_SNAPSHOTS)}),nt=p.object({action:p.literal(ee.DELETE_SNAPSHOT),snapshotId:p.string().uuid()}),te=e=>async({request:t,params:s})=>{E(s.projectId),X(t);const o=await t.json();if(ot.safeParse(o).success)return e.GET("/api/projects/{project_id}/reload",{params:{path:{project_id:s.projectId}}}).then(u({notThrowExc:!0}));const i=nt.safeParse(o);return i.success?e.DELETE("/api/projects/{project_id}/{snapshot_id}",{params:{path:{project_id:s.projectId,snapshot_id:i.data.snapshotId}}}).then(u({notThrowExc:!0})):{error:{status_code:!1,detail:"Unknown action"}}},it=({api:e})=>({loader:({params:t})=>(E(t.projectId),t.snapshotId?Promise.resolve([]):e.GET("/api/projects/{project_id}/reports",{params:{path:{project_id:t.projectId}}}).then(u())),action:te(e)}),at=({api:e})=>({loader:({params:t})=>(E(t.projectId),t.snapshotId?Promise.resolve([]):e.GET("/api/projects/{project_id}/test_suites",{params:{path:{project_id:t.projectId}}}).then(u())),action:te(e)}),ct=({api:e})=>({loader:({params:t})=>{const{projectId:s,snapshotId:o}=t;return E(s),E(o),e.GET("/api/projects/{project_id}/{snapshot_id}/data",{params:{path:{project_id:s,snapshot_id:o}},parseAs:"text"}).then(u()).then(Z)}}),{loader:ht}=ct({api:C}),re={path:":snapshotId",lazy:async()=>{const{SnapshotTemplate:e,...t}=await _(()=>import("./index-DDgANbm4.js"),__vite__mapDeps([6,1,5,3]));return{Component:()=>r.jsx(e,{api:C}),...t}},loader:ht,ErrorBoundary:v},{loader:lt,action:dt}=it({api:C}),ut={id:"reports",path:"reports",lazy:async()=>{const{SnapshotsListTemplate:e,...t}=await _(()=>import("./index-LT2YNxwo.js"),__vite__mapDeps([7,1]));return{...t,Component:()=>r.jsxs(r.Fragment,{children:[r.jsx(B,{}),r.jsx(e,{type:"reports"})]})}},loader:lt,action:dt,ErrorBoundary:v,children:[re]},{loader:pt,action:mt}=at({api:C}),ft={id:"test_suites",path:"test-suites",lazy:async()=>{const{SnapshotsListTemplate:e,...t}=await _(()=>import("./index-LT2YNxwo.js"),__vite__mapDeps([7,1]));return{...t,Component:()=>r.jsxs(r.Fragment,{children:[r.jsx(B,{}),r.jsx(e,{type:"test suites"})]})}},loader:pt,action:mt,ErrorBoundary:v,children:[re]},{loader:jt}=Qe({api:C}),xt={path:"projects/:projectId",lazy:()=>_(()=>import("./index-qb_niS19.js"),__vite__mapDeps([8,1])),loader:jt,ErrorBoundary:v,children:[st,ut,ft]},Lt=p.object({action:p.literal("edit-project")}),yt=p.object({action:p.literal("create-new-project")}),gt=p.object({action:p.literal("delete-project"),projectId:p.string().uuid()}),_t=({api:e})=>({loader:()=>e.GET("/api/projects").then(u()).then(t=>t.map(K)),action:async({request:t})=>{X(t);const s=await t.json();if(yt.safeParse(s).success)return e.POST("/api/projects",{body:s}).then(u({notThrowExc:!0}));const o=gt.safeParse(s);if(o.success)return e.DELETE("/api/projects/{project_id}",{params:{path:{project_id:o.data.projectId}}}).then(u({notThrowExc:!0}));if(Lt.safeParse(s).success)return e.POST("/api/projects/{project_id}/info",{params:{path:{project_id:s.id}},body:s}).then(u({notThrowExc:!0}));throw"Undefined action"}}),{loader:vt,action:Ct}=_t({api:C}),St={index:!0,lazy:()=>_(()=>import("./index-DJhIIsZf.js"),__vite__mapDeps([9,1])).then(e=>({...e,Component:()=>r.jsxs(r.Fragment,{children:[r.jsx(B,{}),r.jsx(e.Component,{})]})})),loader:vt,action:Ct,ErrorBoundary:v},Et={...qe,children:[St,xt,Be],ErrorBoundary:v},bt=Oe([Et]),G=document.getElementById("root");G&&Ae.createRoot(G).render(r.jsx(M.StrictMode,{children:r.jsxs(De,{theme:Fe,children:[r.jsx(Re,{}),r.jsx(Me,{router:bt})]})}));export{N as A,Pt as D,Z as J,wt as a,u as r,Q as u};