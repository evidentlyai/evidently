import{d as F,g as Z,e as P,j as d,u as Ot,L as Ct,f as jt,h as Bt,O as At}from"./vendor-20fe28cb.js";import{d as x,b as wt,r as St,L as _t}from"./LocalizationProvider-c3bcf585.js";import{_ as T,g as lt,a as ct,s as U,c as J,u as dt,b as st,d as ut,e as ht,f as zt,B as Pt,h as at,T as ft,i as It,j as pt,r as Ht,k as Ut,I as $t,l as Ft,m as Nt}from"./createSvgIcon-0f0d4578.js";import{L as Rt,T as Wt,a as Et}from"./Toolbar-d109dc32.js";import{P as mt,B as Jt}from"./Button-7e4968e4.js";import{L as rt}from"./Link-f0cc2b13.js";var yt={exports:{}};(function(r,s){(function(n,a){r.exports=a()})(F,function(){var n="week",a="year";return function(u,t,e){var o=t.prototype;o.week=function(c){if(c===void 0&&(c=null),c!==null)return this.add(7*(c-this.week()),"day");var l=this.$locale().yearStart||1;if(this.month()===11&&this.date()>25){var h=e(this).startOf(a).add(1,a).date(l),y=e(this).endOf(n);if(h.isBefore(y))return 1}var M=e(this).startOf(a).date(l).startOf(n).subtract(1,"millisecond"),j=this.diff(M,n,!0);return j<0?e(this).startOf("week").week():Math.ceil(j)},o.weeks=function(c){return c===void 0&&(c=null),this.week(c)}}})})(yt);var Zt=yt.exports;const Vt=Z(Zt);var gt={exports:{}};(function(r,s){(function(n,a){r.exports=a()})(F,function(){var n={LTS:"h:mm:ss A",LT:"h:mm A",L:"MM/DD/YYYY",LL:"MMMM D, YYYY",LLL:"MMMM D, YYYY h:mm A",LLLL:"dddd, MMMM D, YYYY h:mm A"},a=/(\[[^[]*\])|([-_:/.,()\s]+)|(A|a|YYYY|YY?|MM?M?M?|Do|DD?|hh?|HH?|mm?|ss?|S{1,3}|z|ZZ?)/g,u=/\d\d/,t=/\d\d?/,e=/\d*[^-_:/,()\s\d]+/,o={},c=function(i){return(i=+i)+(i>68?1900:2e3)},l=function(i){return function(f){this[i]=+f}},h=[/[+-]\d\d:?(\d\d)?|Z/,function(i){(this.zone||(this.zone={})).offset=function(f){if(!f||f==="Z")return 0;var p=f.match(/([+-]|\d\d)/g),m=60*p[1]+(+p[2]||0);return m===0?0:p[0]==="+"?-m:m}(i)}],y=function(i){var f=o[i];return f&&(f.indexOf?f:f.s.concat(f.f))},M=function(i,f){var p,m=o.meridiem;if(m){for(var D=1;D<=24;D+=1)if(i.indexOf(m(D,0,f))>-1){p=D>12;break}}else p=i===(f?"pm":"PM");return p},j={A:[e,function(i){this.afternoon=M(i,!1)}],a:[e,function(i){this.afternoon=M(i,!0)}],S:[/\d/,function(i){this.milliseconds=100*+i}],SS:[u,function(i){this.milliseconds=10*+i}],SSS:[/\d{3}/,function(i){this.milliseconds=+i}],s:[t,l("seconds")],ss:[t,l("seconds")],m:[t,l("minutes")],mm:[t,l("minutes")],H:[t,l("hours")],h:[t,l("hours")],HH:[t,l("hours")],hh:[t,l("hours")],D:[t,l("day")],DD:[u,l("day")],Do:[e,function(i){var f=o.ordinal,p=i.match(/\d+/);if(this.day=p[0],f)for(var m=1;m<=31;m+=1)f(m).replace(/\[|\]/g,"")===i&&(this.day=m)}],M:[t,l("month")],MM:[u,l("month")],MMM:[e,function(i){var f=y("months"),p=(y("monthsShort")||f.map(function(m){return m.slice(0,3)})).indexOf(i)+1;if(p<1)throw new Error;this.month=p%12||p}],MMMM:[e,function(i){var f=y("months").indexOf(i)+1;if(f<1)throw new Error;this.month=f%12||f}],Y:[/[+-]?\d+/,l("year")],YY:[u,function(i){this.year=c(i)}],YYYY:[/\d{4}/,l("year")],Z:h,ZZ:h};function $(i){var f,p;f=i,p=o&&o.formats;for(var m=(i=f.replace(/(\[[^\]]+])|(LTS?|l{1,4}|L{1,4})/g,function(O,B,C){var L=C&&C.toUpperCase();return B||p[C]||n[C]||p[L].replace(/(\[[^\]]+])|(MMMM|MM|DD|dddd)/g,function(A,w,_){return w||_.slice(1)})})).match(a),D=m.length,Y=0;Y<D;Y+=1){var S=m[Y],k=j[S],g=k&&k[0],b=k&&k[1];m[Y]=b?{regex:g,parser:b}:S.replace(/^\[|\]$/g,"")}return function(O){for(var B={},C=0,L=0;C<D;C+=1){var A=m[C];if(typeof A=="string")L+=A.length;else{var w=A.regex,_=A.parser,N=O.slice(L),I=w.exec(N)[0];_.call(B,I),O=O.replace(I,"")}}return function(z){var v=z.afternoon;if(v!==void 0){var H=z.hours;v?H<12&&(z.hours+=12):H===12&&(z.hours=0),delete z.afternoon}}(B),B}}return function(i,f,p){p.p.customParseFormat=!0,i&&i.parseTwoDigitYear&&(c=i.parseTwoDigitYear);var m=f.prototype,D=m.parse;m.parse=function(Y){var S=Y.date,k=Y.utc,g=Y.args;this.$u=k;var b=g[1];if(typeof b=="string"){var O=g[2]===!0,B=g[3]===!0,C=O||B,L=g[2];B&&(L=g[2]),o=this.$locale(),!O&&L&&(o=p.Ls[L]),this.$d=function(N,I,z){try{if(["x","X"].indexOf(I)>-1)return new Date((I==="X"?1e3:1)*N);var v=$(I)(N),H=v.year,R=v.month,bt=v.day,Yt=v.hours,kt=v.minutes,Lt=v.seconds,vt=v.milliseconds,nt=v.zone,V=new Date,q=bt||(H||R?1:V.getDate()),G=H||V.getFullYear(),W=0;H&&!R||(W=R>0?R-1:V.getMonth());var X=Yt||0,K=kt||0,Q=Lt||0,tt=vt||0;return nt?new Date(Date.UTC(G,W,q,X,K,Q,tt+60*nt.offset*1e3)):z?new Date(Date.UTC(G,W,q,X,K,Q,tt)):new Date(G,W,q,X,K,Q,tt)}catch{return new Date("")}}(S,b,k),this.init(),L&&L!==!0&&(this.$L=this.locale(L).$L),C&&S!=this.format(b)&&(this.$d=new Date("")),o={}}else if(b instanceof Array)for(var A=b.length,w=1;w<=A;w+=1){g[1]=b[w-1];var _=p.apply(this,g);if(_.isValid()){this.$d=_.$d,this.$L=_.$L,this.init();break}w===A&&(this.$d=new Date(""))}else D.call(this,Y)}}})})(gt);var qt=gt.exports;const Gt=Z(qt);var Mt={exports:{}};(function(r,s){(function(n,a){r.exports=a()})(F,function(){var n={LTS:"h:mm:ss A",LT:"h:mm A",L:"MM/DD/YYYY",LL:"MMMM D, YYYY",LLL:"MMMM D, YYYY h:mm A",LLLL:"dddd, MMMM D, YYYY h:mm A"};return function(a,u,t){var e=u.prototype,o=e.format;t.en.formats=n,e.format=function(c){c===void 0&&(c="YYYY-MM-DDTHH:mm:ssZ");var l=this.$locale().formats,h=function(y,M){return y.replace(/(\[[^\]]+])|(LTS?|l{1,4}|L{1,4})/g,function(j,$,i){var f=i&&i.toUpperCase();return $||M[i]||n[i]||M[f].replace(/(\[[^\]]+])|(MMMM|MM|DD|dddd)/g,function(p,m,D){return m||D.slice(1)})})}(c,l===void 0?{}:l);return o.call(this,h)}}})})(Mt);var Xt=Mt.exports;const Kt=Z(Xt);var xt={exports:{}};(function(r,s){(function(n,a){r.exports=a()})(F,function(){return function(n,a,u){a.prototype.isBetween=function(t,e,o,c){var l=u(t),h=u(e),y=(c=c||"()")[0]==="(",M=c[1]===")";return(y?this.isAfter(l,o):!this.isBefore(l,o))&&(M?this.isBefore(h,o):!this.isAfter(h,o))||(y?this.isBefore(l,o):!this.isAfter(l,o))&&(M?this.isAfter(h,o):!this.isBefore(h,o))}}})})(xt);var Qt=xt.exports;const te=Z(Qt);x.extend(Gt);x.extend(Kt);x.extend(te);const ee=wt(["Your locale has not been found.","Either the locale key is not a supported one. Locales supported by dayjs are available here: https://github.com/iamkun/dayjs/tree/dev/src/locale","Or you forget to import the locale from 'dayjs/locale/{localeUsed}'","fallback on English locale"]),re={YY:"year",YYYY:{sectionType:"year",contentType:"digit",maxLength:4},M:{sectionType:"month",contentType:"digit",maxLength:2},MM:"month",MMM:{sectionType:"month",contentType:"letter"},MMMM:{sectionType:"month",contentType:"letter"},D:{sectionType:"day",contentType:"digit",maxLength:2},DD:"day",Do:{sectionType:"day",contentType:"digit-with-letter"},d:{sectionType:"weekDay",contentType:"digit",maxLength:2},dd:{sectionType:"weekDay",contentType:"letter"},ddd:{sectionType:"weekDay",contentType:"letter"},dddd:{sectionType:"weekDay",contentType:"letter"},A:"meridiem",a:"meridiem",H:{sectionType:"hours",contentType:"digit",maxLength:2},HH:"hours",h:{sectionType:"hours",contentType:"digit",maxLength:2},hh:"hours",m:{sectionType:"minutes",contentType:"digit",maxLength:2},mm:"minutes",s:{sectionType:"seconds",contentType:"digit",maxLength:2},ss:"seconds"},se={year:"YYYY",month:"MMMM",monthShort:"MMM",dayOfMonth:"D",weekday:"dddd",weekdayShort:"ddd",hours24h:"HH",hours12h:"hh",meridiem:"A",minutes:"mm",seconds:"ss",fullDate:"ll",fullDateWithWeekday:"dddd, LL",keyboardDate:"L",shortDate:"MMM D",normalDate:"D MMMM",normalDateWithWeekday:"ddd, MMM D",monthAndYear:"MMMM YYYY",monthAndDate:"MMMM D",fullTime:"LT",fullTime12h:"hh:mm A",fullTime24h:"HH:mm",fullDateTime:"lll",fullDateTime12h:"ll hh:mm A",fullDateTime24h:"ll HH:mm",keyboardDateTime:"L LT",keyboardDateTime12h:"L hh:mm A",keyboardDateTime24h:"L HH:mm"},et=["Missing UTC plugin","To be able to use UTC or timezones, you have to enable the `utc` plugin","Find more information on https://mui.com/x/react-date-pickers/timezone/#day-js-and-utc"].join(`
`),it=["Missing timezone plugin","To be able to use timezones, you have to enable both the `utc` and the `timezone` plugin","Find more information on https://mui.com/x/react-date-pickers/timezone/#day-js-and-timezone"].join(`
`),oe=(r,s)=>s?(...n)=>r(...n).locale(s):r;class ne{constructor({locale:s,formats:n,instance:a}={}){var u;this.isMUIAdapter=!0,this.isTimezoneCompatible=!0,this.lib="dayjs",this.rawDayJsInstance=void 0,this.dayjs=void 0,this.locale=void 0,this.formats=void 0,this.escapedCharacters={start:"[",end:"]"},this.formatTokenMap=re,this.setLocaleToValue=t=>{const e=this.getCurrentLocaleCode();return e===t.locale()?t:t.locale(e)},this.hasUTCPlugin=()=>typeof x.utc<"u",this.hasTimezonePlugin=()=>typeof x.tz<"u",this.isSame=(t,e,o)=>{const c=this.setTimezone(e,this.getTimezone(t));return t.format(o)===c.format(o)},this.cleanTimezone=t=>{switch(t){case"default":return;case"system":return x.tz.guess();default:return t}},this.createSystemDate=t=>{if(this.rawDayJsInstance)return this.rawDayJsInstance(t);if(this.hasUTCPlugin()&&this.hasTimezonePlugin()){const e=x.tz.guess();return e!=="UTC"?x.tz(t,e):x(t)}return x(t)},this.createUTCDate=t=>{if(!this.hasUTCPlugin())throw new Error(et);return x.utc(t)},this.createTZDate=(t,e)=>{if(!this.hasUTCPlugin())throw new Error(et);if(!this.hasTimezonePlugin())throw new Error(it);const o=t!==void 0&&!t.endsWith("Z");return x(t).tz(this.cleanTimezone(e),o)},this.getLocaleFormats=()=>{const t=x.Ls,e=this.locale||"en";let o=t[e];return o===void 0&&(ee(),o=t.en),o.formats},this.adjustOffset=t=>{if(!this.hasTimezonePlugin())return t;const e=this.getTimezone(t);if(e!=="UTC"){var o,c;const l=t.tz(this.cleanTimezone(e),!0);return((o=l.$offset)!=null?o:0)===((c=t.$offset)!=null?c:0)?t:l}return t},this.date=t=>t===null?null:this.dayjs(t),this.dateWithTimezone=(t,e)=>{if(t===null)return null;let o;return e==="UTC"?o=this.createUTCDate(t):e==="system"||e==="default"&&!this.hasTimezonePlugin()?o=this.createSystemDate(t):o=this.createTZDate(t,e),this.locale===void 0?o:o.locale(this.locale)},this.getTimezone=t=>{if(this.hasTimezonePlugin()){var e;const o=(e=t.$x)==null?void 0:e.$timezone;if(o)return o}return this.hasUTCPlugin()&&t.isUTC()?"UTC":"system"},this.setTimezone=(t,e)=>{if(this.getTimezone(t)===e)return t;if(e==="UTC"){if(!this.hasUTCPlugin())throw new Error(et);return t.utc()}if(e==="system")return t.local();if(!this.hasTimezonePlugin()){if(e==="default")return t;throw new Error(it)}return x.tz(t,this.cleanTimezone(e))},this.toJsDate=t=>t.toDate(),this.parseISO=t=>this.dayjs(t),this.toISO=t=>t.toISOString(),this.parse=(t,e)=>t===""?null:this.dayjs(t,e,this.locale,!0),this.getCurrentLocaleCode=()=>this.locale||"en",this.is12HourCycleInCurrentLocale=()=>/A|a/.test(this.getLocaleFormats().LT||""),this.expandFormat=t=>{const e=this.getLocaleFormats(),o=c=>c.replace(/(\[[^\]]+])|(MMMM|MM|DD|dddd)/g,(l,h,y)=>h||y.slice(1));return t.replace(/(\[[^\]]+])|(LTS?|l{1,4}|L{1,4})/g,(c,l,h)=>{const y=h&&h.toUpperCase();return l||e[h]||o(e[y])})},this.getFormatHelperText=t=>this.expandFormat(t).replace(/a/gi,"(a|p)m").toLocaleLowerCase(),this.isNull=t=>t===null,this.isValid=t=>this.dayjs(t).isValid(),this.format=(t,e)=>this.formatByString(t,this.formats[e]),this.formatByString=(t,e)=>this.dayjs(t).format(e),this.formatNumber=t=>t,this.getDiff=(t,e,o)=>t.diff(e,o),this.isEqual=(t,e)=>t===null&&e===null?!0:this.dayjs(t).toDate().getTime()===this.dayjs(e).toDate().getTime(),this.isSameYear=(t,e)=>this.isSame(t,e,"YYYY"),this.isSameMonth=(t,e)=>this.isSame(t,e,"YYYY-MM"),this.isSameDay=(t,e)=>this.isSame(t,e,"YYYY-MM-DD"),this.isSameHour=(t,e)=>t.isSame(e,"hour"),this.isAfter=(t,e)=>t>e,this.isAfterYear=(t,e)=>this.hasUTCPlugin()?!this.isSameYear(t,e)&&t.utc()>e.utc():t.isAfter(e,"year"),this.isAfterDay=(t,e)=>this.hasUTCPlugin()?!this.isSameDay(t,e)&&t.utc()>e.utc():t.isAfter(e,"day"),this.isBefore=(t,e)=>t<e,this.isBeforeYear=(t,e)=>this.hasUTCPlugin()?!this.isSameYear(t,e)&&t.utc()<e.utc():t.isBefore(e,"year"),this.isBeforeDay=(t,e)=>this.hasUTCPlugin()?!this.isSameDay(t,e)&&t.utc()<e.utc():t.isBefore(e,"day"),this.isWithinRange=(t,[e,o])=>t>=e&&t<=o,this.startOfYear=t=>this.adjustOffset(t.startOf("year")),this.startOfMonth=t=>this.adjustOffset(t.startOf("month")),this.startOfWeek=t=>this.adjustOffset(t.startOf("week")),this.startOfDay=t=>this.adjustOffset(t.startOf("day")),this.endOfYear=t=>this.adjustOffset(t.endOf("year")),this.endOfMonth=t=>this.adjustOffset(t.endOf("month")),this.endOfWeek=t=>this.adjustOffset(t.endOf("week")),this.endOfDay=t=>this.adjustOffset(t.endOf("day")),this.addYears=(t,e)=>this.adjustOffset(e<0?t.subtract(Math.abs(e),"year"):t.add(e,"year")),this.addMonths=(t,e)=>this.adjustOffset(e<0?t.subtract(Math.abs(e),"month"):t.add(e,"month")),this.addWeeks=(t,e)=>this.adjustOffset(e<0?t.subtract(Math.abs(e),"week"):t.add(e,"week")),this.addDays=(t,e)=>this.adjustOffset(e<0?t.subtract(Math.abs(e),"day"):t.add(e,"day")),this.addHours=(t,e)=>this.adjustOffset(e<0?t.subtract(Math.abs(e),"hour"):t.add(e,"hour")),this.addMinutes=(t,e)=>this.adjustOffset(e<0?t.subtract(Math.abs(e),"minute"):t.add(e,"minute")),this.addSeconds=(t,e)=>this.adjustOffset(e<0?t.subtract(Math.abs(e),"second"):t.add(e,"second")),this.getYear=t=>t.year(),this.getMonth=t=>t.month(),this.getDate=t=>t.date(),this.getHours=t=>t.hour(),this.getMinutes=t=>t.minute(),this.getSeconds=t=>t.second(),this.getMilliseconds=t=>t.millisecond(),this.setYear=(t,e)=>this.adjustOffset(t.set("year",e)),this.setMonth=(t,e)=>this.adjustOffset(t.set("month",e)),this.setDate=(t,e)=>this.adjustOffset(t.set("date",e)),this.setHours=(t,e)=>this.adjustOffset(t.set("hour",e)),this.setMinutes=(t,e)=>this.adjustOffset(t.set("minute",e)),this.setSeconds=(t,e)=>this.adjustOffset(t.set("second",e)),this.setMilliseconds=(t,e)=>this.adjustOffset(t.set("millisecond",e)),this.getDaysInMonth=t=>t.daysInMonth(),this.getNextMonth=t=>this.addMonths(t,1),this.getPreviousMonth=t=>this.addMonths(t,-1),this.getMonthArray=t=>{const o=[t.startOf("year")];for(;o.length<12;){const c=o[o.length-1];o.push(this.addMonths(c,1))}return o},this.mergeDateAndTime=(t,e)=>t.hour(e.hour()).minute(e.minute()).second(e.second()),this.getWeekdays=()=>{const t=this.dayjs().startOf("week");return[0,1,2,3,4,5,6].map(e=>this.formatByString(this.addDays(t,e),"dd"))},this.getWeekArray=t=>{const e=this.setLocaleToValue(t),o=e.startOf("month").startOf("week"),c=e.endOf("month").endOf("week");let l=0,h=o;const y=[];for(;h<c;){const M=Math.floor(l/7);y[M]=y[M]||[],y[M].push(h),h=this.addDays(h,1),l+=1}return y},this.getWeekNumber=t=>t.week(),this.getYearRange=(t,e)=>{const o=t.startOf("year"),c=e.endOf("year"),l=[];let h=o;for(;h<c;)l.push(h),h=this.addYears(h,1);return l},this.getMeridiemText=t=>t==="am"?"AM":"PM",this.rawDayJsInstance=a,this.dayjs=oe((u=this.rawDayJsInstance)!=null?u:x,s),this.locale=s,this.formats=T({},se,n),x.extend(Vt)}}var ae={exports:{}};(function(r,s){(function(n,a){r.exports=a(St())})(F,function(n){function a(e){return e&&typeof e=="object"&&"default"in e?e:{default:e}}var u=a(n),t={name:"en-gb",weekdays:"Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),weekdaysShort:"Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),weekdaysMin:"Su_Mo_Tu_We_Th_Fr_Sa".split("_"),months:"January_February_March_April_May_June_July_August_September_October_November_December".split("_"),monthsShort:"Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),weekStart:1,yearStart:4,relativeTime:{future:"in %s",past:"%s ago",s:"a few seconds",m:"a minute",mm:"%d minutes",h:"an hour",hh:"%d hours",d:"a day",dd:"%d days",M:"a month",MM:"%d months",y:"a year",yy:"%d years"},formats:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},ordinal:function(e){var o=["th","st","nd","rd"],c=e%100;return"["+e+(o[(c-20)%10]||o[c]||o[0])+"]"}};return u.default.locale(t,null,!0),t})})(ae);function ie(r){return lt("MuiAppBar",r)}ct("MuiAppBar",["root","positionFixed","positionAbsolute","positionSticky","positionStatic","positionRelative","colorDefault","colorPrimary","colorSecondary","colorInherit","colorTransparent"]);const le=["className","color","enableColorOnDark","position"],ce=r=>{const{color:s,position:n,classes:a}=r,u={root:["root",`color${J(s)}`,`position${J(n)}`]};return ht(u,ie,a)},E=(r,s)=>r?`${r==null?void 0:r.replace(")","")}, ${s})`:s,de=U(mt,{name:"MuiAppBar",slot:"Root",overridesResolver:(r,s)=>{const{ownerState:n}=r;return[s.root,s[`position${J(n.position)}`],s[`color${J(n.color)}`]]}})(({theme:r,ownerState:s})=>{const n=r.palette.mode==="light"?r.palette.grey[100]:r.palette.grey[900];return T({display:"flex",flexDirection:"column",width:"100%",boxSizing:"border-box",flexShrink:0},s.position==="fixed"&&{position:"fixed",zIndex:(r.vars||r).zIndex.appBar,top:0,left:"auto",right:0,"@media print":{position:"absolute"}},s.position==="absolute"&&{position:"absolute",zIndex:(r.vars||r).zIndex.appBar,top:0,left:"auto",right:0},s.position==="sticky"&&{position:"sticky",zIndex:(r.vars||r).zIndex.appBar,top:0,left:"auto",right:0},s.position==="static"&&{position:"static"},s.position==="relative"&&{position:"relative"},!r.vars&&T({},s.color==="default"&&{backgroundColor:n,color:r.palette.getContrastText(n)},s.color&&s.color!=="default"&&s.color!=="inherit"&&s.color!=="transparent"&&{backgroundColor:r.palette[s.color].main,color:r.palette[s.color].contrastText},s.color==="inherit"&&{color:"inherit"},r.palette.mode==="dark"&&!s.enableColorOnDark&&{backgroundColor:null,color:null},s.color==="transparent"&&T({backgroundColor:"transparent",color:"inherit"},r.palette.mode==="dark"&&{backgroundImage:"none"})),r.vars&&T({},s.color==="default"&&{"--AppBar-background":s.enableColorOnDark?r.vars.palette.AppBar.defaultBg:E(r.vars.palette.AppBar.darkBg,r.vars.palette.AppBar.defaultBg),"--AppBar-color":s.enableColorOnDark?r.vars.palette.text.primary:E(r.vars.palette.AppBar.darkColor,r.vars.palette.text.primary)},s.color&&!s.color.match(/^(default|inherit|transparent)$/)&&{"--AppBar-background":s.enableColorOnDark?r.vars.palette[s.color].main:E(r.vars.palette.AppBar.darkBg,r.vars.palette[s.color].main),"--AppBar-color":s.enableColorOnDark?r.vars.palette[s.color].contrastText:E(r.vars.palette.AppBar.darkColor,r.vars.palette[s.color].contrastText)},{backgroundColor:"var(--AppBar-background)",color:s.color==="inherit"?"inherit":"var(--AppBar-color)"},s.color==="transparent"&&{backgroundImage:"none",backgroundColor:"transparent",color:"inherit"}))}),ue=P.forwardRef(function(s,n){const a=dt({props:s,name:"MuiAppBar"}),{className:u,color:t="primary",enableColorOnDark:e=!1,position:o="fixed"}=a,c=st(a,le),l=T({},a,{color:t,position:o,enableColorOnDark:e}),h=ce(l);return d.jsx(de,T({square:!0,component:"header",ownerState:l,elevation:4,className:ut(h.root,u,o==="fixed"&&"mui-fixed"),ref:n},c))}),he=ue,fe=zt(d.jsx("path",{d:"M6 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm12 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-6 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"}),"MoreHoriz"),pe=["slots","slotProps"],me=U(Pt)(({theme:r})=>T({display:"flex",marginLeft:`calc(${r.spacing(1)} * 0.5)`,marginRight:`calc(${r.spacing(1)} * 0.5)`},r.palette.mode==="light"?{backgroundColor:r.palette.grey[100],color:r.palette.grey[700]}:{backgroundColor:r.palette.grey[700],color:r.palette.grey[100]},{borderRadius:2,"&:hover, &:focus":T({},r.palette.mode==="light"?{backgroundColor:r.palette.grey[200]}:{backgroundColor:r.palette.grey[600]}),"&:active":T({boxShadow:r.shadows[0]},r.palette.mode==="light"?{backgroundColor:at(r.palette.grey[200],.12)}:{backgroundColor:at(r.palette.grey[600],.12)})})),ye=U(fe)({width:24,height:16});function ge(r){const{slots:s={},slotProps:n={}}=r,a=st(r,pe),u=r;return d.jsx("li",{children:d.jsx(me,T({focusRipple:!0},a,{ownerState:u,children:d.jsx(ye,T({as:s.CollapsedIcon,ownerState:u},n.collapsedIcon))}))})}function Me(r){return lt("MuiBreadcrumbs",r)}const xe=ct("MuiBreadcrumbs",["root","ol","li","separator"]),Te=xe,De=["children","className","component","slots","slotProps","expandText","itemsAfterCollapse","itemsBeforeCollapse","maxItems","separator"],be=r=>{const{classes:s}=r;return ht({root:["root"],li:["li"],ol:["ol"],separator:["separator"]},Me,s)},Ye=U(ft,{name:"MuiBreadcrumbs",slot:"Root",overridesResolver:(r,s)=>[{[`& .${Te.li}`]:s.li},s.root]})({}),ke=U("ol",{name:"MuiBreadcrumbs",slot:"Ol",overridesResolver:(r,s)=>s.ol})({display:"flex",flexWrap:"wrap",alignItems:"center",padding:0,margin:0,listStyle:"none"}),Le=U("li",{name:"MuiBreadcrumbs",slot:"Separator",overridesResolver:(r,s)=>s.separator})({display:"flex",userSelect:"none",marginLeft:8,marginRight:8});function ve(r,s,n,a){return r.reduce((u,t,e)=>(e<r.length-1?u=u.concat(t,d.jsx(Le,{"aria-hidden":!0,className:s,ownerState:a,children:n},`separator-${e}`)):u.push(t),u),[])}const Oe=P.forwardRef(function(s,n){const a=dt({props:s,name:"MuiBreadcrumbs"}),{children:u,className:t,component:e="nav",slots:o={},slotProps:c={},expandText:l="Show path",itemsAfterCollapse:h=1,itemsBeforeCollapse:y=1,maxItems:M=8,separator:j="/"}=a,$=st(a,De),[i,f]=P.useState(!1),p=T({},a,{component:e,expanded:i,expandText:l,itemsAfterCollapse:h,itemsBeforeCollapse:y,maxItems:M,separator:j}),m=be(p),D=It({elementType:o.CollapsedIcon,externalSlotProps:c.collapsedIcon,ownerState:p}),Y=P.useRef(null),S=g=>{const b=()=>{f(!0);const O=Y.current.querySelector("a[href],button,[tabindex]");O&&O.focus()};return y+h>=g.length?g:[...g.slice(0,y),d.jsx(ge,{"aria-label":l,slots:{CollapsedIcon:o.CollapsedIcon},slotProps:{collapsedIcon:D},onClick:b},"ellipsis"),...g.slice(g.length-h,g.length)]},k=P.Children.toArray(u).filter(g=>P.isValidElement(g)).map((g,b)=>d.jsx("li",{className:m.li,children:g},`child-${b}`));return d.jsx(Ye,T({ref:n,component:e,color:"text.secondary",className:ut(m.root,t),ownerState:p},$,{children:d.jsx(ke,{className:m.ol,ref:Y,ownerState:p,children:ve(i||M&&k.length<=M?k:S(k),m.separator,j,p)})}))}),Ce=Oe,je=r=>{var s;return typeof((s=r==null?void 0:r.handle)==null?void 0:s.crumb)=="function"},Be=()=>{const s=Ot().filter(je).map(({handle:n,data:a,id:u,pathname:t,params:e})=>n.crumb(a,{id:u,pathname:t,params:e}));return d.jsx(pt,{children:d.jsx(Ce,{"aria-label":"breadcrumb",children:s.map(n=>d.jsx(rt,{component:Ct,color:"inherit",to:n.to,children:n.linkText},n.to))})})},Ae=()=>jt().state!=="idle"?d.jsx(Rt,{sx:{height:4}}):d.jsx(pt,{sx:{height:4}}),we="/static/img/logo-01c8a56e.png";var ot={},Se=Ut;Object.defineProperty(ot,"__esModule",{value:!0});var Tt=ot.default=void 0;Pe(P);var _e=Se(Ht()),ze=d;function Dt(r){if(typeof WeakMap!="function")return null;var s=new WeakMap,n=new WeakMap;return(Dt=function(a){return a?n:s})(r)}function Pe(r,s){if(!s&&r&&r.__esModule)return r;if(r===null||typeof r!="object"&&typeof r!="function")return{default:r};var n=Dt(s);if(n&&n.has(r))return n.get(r);var a={},u=Object.defineProperty&&Object.getOwnPropertyDescriptor;for(var t in r)if(t!=="default"&&Object.prototype.hasOwnProperty.call(r,t)){var e=u?Object.getOwnPropertyDescriptor(r,t):null;e&&(e.get||e.set)?Object.defineProperty(a,t,e):a[t]=r[t]}return a.default=r,n&&n.set(r,a),a}var Ie=(0,_e.default)((0,ze.jsx)("path",{d:"M12 1.27a11 11 0 00-3.48 21.46c.55.09.73-.28.73-.55v-1.84c-3.03.64-3.67-1.46-3.67-1.46-.55-1.29-1.28-1.65-1.28-1.65-.92-.65.1-.65.1-.65 1.1 0 1.73 1.1 1.73 1.1.92 1.65 2.57 1.2 3.21.92a2 2 0 01.64-1.47c-2.47-.27-5.04-1.19-5.04-5.5 0-1.1.46-2.1 1.2-2.84a3.76 3.76 0 010-2.93s.91-.28 3.11 1.1c1.8-.49 3.7-.49 5.5 0 2.1-1.38 3.02-1.1 3.02-1.1a3.76 3.76 0 010 2.93c.83.74 1.2 1.74 1.2 2.94 0 4.21-2.57 5.13-5.04 5.4.45.37.82.92.82 2.02v3.03c0 .27.1.64.73.55A11 11 0 0012 1.27"}),"GitHub");Tt=ot.default=Ie;function He({version:r}){return d.jsx(d.Fragment,{children:d.jsx(he,{position:"static",color:"transparent",children:d.jsxs(Wt,{children:[d.jsxs(ft,{variant:"h6",sx:{flexGrow:1},children:[d.jsx("img",{src:we,height:"55px"}),d.jsx("span",{style:{verticalAlign:"super",fontSize:"0.75rem"},children:r})]}),d.jsx(rt,{href:"https://github.com/evidentlyai/evidently",children:d.jsx($t,{children:d.jsx(Tt,{})})}),d.jsx(rt,{href:"https://docs.evidentlyai.com/",children:d.jsx(Jt,{children:"Docs"})})]})})})}function Ue(r){return d.jsx(d.Fragment,{children:d.jsxs(mt,{sx:{marginTop:"20px",marginLeft:"10px",marginRight:"10px",padding:"10px"},children:[d.jsx(Be,{}),r.children]})})}const $e=Ft({shape:{borderRadius:0},palette:{primary:{light:"#ed5455",main:"#ed0400",dark:"#d40400",contrastText:"#fff"},secondary:{light:"#61a0ff",main:"#3c7fdd",dark:"#61a0ff",contrastText:"#000"}},typography:{button:{fontWeight:"bold"},fontFamily:["-apple-system","BlinkMacSystemFont",'"Segoe UI"',"Roboto",'"Helvetica Neue"',"Arial","sans-serif",'"Apple Color Emoji"','"Segoe UI Emoji"','"Segoe UI Symbol"'].join(",")}}),Ve=()=>Nt.getVersion(),qe=()=>{const{version:r}=Bt();return d.jsx(Et,{theme:$e,children:d.jsxs(_t,{dateAdapter:ne,adapterLocale:"en-gb",children:[d.jsx(He,{version:r}),d.jsx(Ae,{}),d.jsx(Ue,{children:d.jsx(At,{})})]})})},Ge={crumb:()=>({to:"/",linkText:"Home"})};export{qe as Component,Ge as handle,Ve as loader};