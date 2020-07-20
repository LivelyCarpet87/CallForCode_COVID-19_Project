(function(g){var window=this;var O5=function(a,b){var c="ytp-miniplayer-button-bottom-right";var d=g.W?{D:"div",Y:["ytp-icon","ytp-icon-expand-watch-page"]}:{D:"svg",P:{height:"18px",version:"1.1",viewBox:"0 0 22 18",width:"22px"},K:[{D:"g",P:{fill:"none","fill-rule":"evenodd",stroke:"none","stroke-width":"1"},K:[{D:"g",P:{transform:"translate(-1.000000, -3.000000)"},K:[{D:"polygon",P:{points:"0 0 24 0 24 24 0 24"}},{D:"path",P:{d:"M19,7 L5,7 L5,17 L19,17 L19,7 Z M23,19 L23,4.98 C23,3.88 22.1,3 21,3 L3,3 C1.9,3 1,3.88 1,4.98 L1,19 C1,20.1 1.9,21 3,21 L21,21 C22.1,21 23,20.1 23,19 Z M21,19.02 L3,19.02 L3,4.97 L21,4.97 L21,19.02 Z",
fill:"#fff","fill-rule":"nonzero"}}]}]}]};var e="Open video page";a.O().ia("kevlar_miniplayer_expand_top")&&(c="ytp-miniplayer-button-top-left",d=g.W?{D:"div",Y:["ytp-icon","ytp-icon-expand-miniplayer"]}:{D:"svg",P:{height:"24px",version:"1.1",viewBox:"0 0 24 24",width:"24px"},K:[{D:"g",P:{fill:"none","fill-rule":"evenodd",stroke:"none","stroke-width":"1"},K:[{D:"g",P:{transform:"translate(12.000000, 12.000000) scale(-1, 1) translate(-12.000000, -12.000000) "},K:[{D:"path",P:{d:"M19,19 L5,19 L5,5 L12,5 L12,3 L5,3 C3.89,3 3,3.9 3,5 L3,19 C3,20.1 3.89,21 5,21 L19,21 C20.1,21 21,20.1 21,19 L21,12 L19,12 L19,19 Z M14,3 L14,5 L17.59,5 L7.76,14.83 L9.17,16.24 L19,6.41 L19,10 L21,10 L21,3 L14,3 Z",
fill:"#fff","fill-rule":"nonzero"}}]}]}]},e="Expand");g.U.call(this,{D:"button",Y:["ytp-miniplayer-expand-watch-page-button","ytp-button",c],P:{title:"{{title}}","data-tooltip-target-id":"ytp-miniplayer-expand-watch-page-button"},K:[d]});this.H=a;this.na("click",this.onClick,this);this.ma("title",g.bO(a,e,"i"));g.Je(this,g.OO(b.tb(),this.element))},P5=function(a){g.U.call(this,{D:"div",
J:"ytp-miniplayer-ui"});this.ol=!1;this.player=a;this.L(a,"minimized",this.Si);this.L(a,"onStateChange",this.mP)},Q5=function(a){g.uN.call(this,a);
this.o=new P5(this.player);this.o.hide();g.gN(this.player,this.o.element,4);a.app.I.o&&(this.load(),g.J(a.getRootNode(),"ytp-player-minimized",!0))};
g.t(O5,g.U);O5.prototype.onClick=function(){this.H.ra("onExpandMiniplayer")};g.t(P5,g.U);g.k=P5.prototype;
g.k.show=function(){this.Gc=new g.sn(this.Hn,null,this);this.Gc.start();if(!this.ol){this.tooltip=new g.$R(this.player,this);g.C(this,this.tooltip);g.gN(this.player,this.tooltip.element,4);this.tooltip.Td=.6;this.rb=new g.HO(this.player);g.C(this,this.rb);this.aj=new g.U({D:"div",J:"ytp-miniplayer-scrim"});g.C(this,this.aj);this.aj.ca(this.element);this.L(this.aj.element,"click",this.vC);var a=new g.U({D:"button",Y:["ytp-miniplayer-close-button","ytp-button"],P:{"aria-label":"Close"},K:[g.cM()]});
g.C(this,a);a.ca(this.aj.element);this.L(a.element,"click",this.Il);a=new O5(this.player,this);g.C(this,a);a.ca(this.aj.element);this.vj=new g.U({D:"div",J:"ytp-miniplayer-controls"});g.C(this,this.vj);this.vj.ca(this.aj.element);this.L(this.vj.element,"click",this.vC);var b=new g.U({D:"div",J:"ytp-miniplayer-button-container"});g.C(this,b);b.ca(this.vj.element);a=new g.U({D:"div",J:"ytp-miniplayer-play-button-container"});g.C(this,a);a.ca(this.vj.element);var c=new g.U({D:"div",J:"ytp-miniplayer-button-container"});
g.C(this,c);c.ca(this.vj.element);this.QC=new g.AQ(this.player,this,!1);g.C(this,this.QC);this.QC.ca(b.element);b=new g.wQ(this.player,this);g.C(this,b);b.ca(a.element);this.nextButton=new g.AQ(this.player,this,!0);g.C(this,this.nextButton);this.nextButton.ca(c.element);this.fg=new g.JR(this.player,this);g.C(this,this.fg);this.fg.ca(this.aj.element);this.fc=new g.JQ(this.player,this);g.C(this,this.fc);g.gN(this.player,this.fc.element,4);this.yq=new g.U({D:"div",J:"ytp-miniplayer-buttons"});g.C(this,
this.yq);g.gN(this.player,this.yq.element,4);a=new g.U({D:"button",Y:["ytp-miniplayer-close-button","ytp-button"],P:{"aria-label":"Close"},K:[g.cM()]});g.C(this,a);a.ca(this.yq.element);this.L(a.element,"click",this.Il);a=new g.U({D:"button",Y:["ytp-miniplayer-replay-button","ytp-button"],P:{"aria-label":"Close"},K:[g.rM()]});g.C(this,a);a.ca(this.yq.element);this.L(a.element,"click",this.nN);this.L(this.player,"presentingplayerstatechange",this.Tb);this.L(this.player,"appresize",this.Oa);this.L(this.player,
"fullscreentoggled",this.Oa);this.Oa();this.ol=!0}0!==this.player.getPlayerState()&&g.U.prototype.show.call(this);this.fc.show();this.player.unloadModule("annotations_module")};
g.k.hide=function(){this.Gc&&(this.Gc.dispose(),this.Gc=void 0);g.U.prototype.hide.call(this);this.player.app.I.o||(this.ol&&this.fc.hide(),this.player.loadModule("annotations_module"))};
g.k.X=function(){this.Gc&&(this.Gc.dispose(),this.Gc=void 0);g.U.prototype.X.call(this)};
g.k.Il=function(){this.player.stopVideo();this.player.ra("onCloseMiniplayer")};
g.k.nN=function(){this.player.playVideo()};
g.k.vC=function(a){if(a.target===this.aj.element||a.target===this.vj.element)g.Q(this.player.O().experiments,"kevlar_miniplayer_play_pause_on_scrim")?g.DC(g.SL(this.player))?this.player.pauseVideo():this.player.playVideo():this.player.ra("onExpandMiniplayer")};
g.k.Si=function(){g.J(this.player.getRootNode(),"ytp-player-minimized",this.player.app.I.o)};
g.k.Yc=function(){this.fc.hc();this.fg.hc()};
g.k.Hn=function(){this.Yc();this.Gc&&this.Gc.start()};
g.k.Tb=function(a){g.T(a.state,32)&&this.tooltip.hide()};
g.k.Oa=function(){this.fc.setPosition(0,g.QM(this.player).getPlayerSize().width,!1);this.fc.Ow()};
g.k.mP=function(a){this.player.app.I.o&&(0===a?this.hide():this.show())};
g.k.tb=function(){return this.tooltip};
g.k.Kc=function(){return!1};
g.k.me=function(){return!1};
g.k.Mf=function(){return!1};
g.k.lw=function(){};
g.k.yj=function(){};
g.k.Gm=function(){};
g.k.Gj=function(){return null};
g.k.fl=function(){return new g.sh(0,0,0,0)};
g.k.handleGlobalKeyDown=function(){return!1};
g.k.handleGlobalKeyUp=function(){return!1};
g.k.Ml=function(a,b,c,d,e){var f=0,h=d=0,l=g.Oh(a);if(b){c=g.Cn(b,"ytp-prev-button")||g.Cn(b,"ytp-next-button");var m=g.Cn(b,"ytp-play-button"),n=g.Cn(b,"ytp-miniplayer-expand-watch-page-button");c?f=h=12:m?(b=g.Lh(b,this.element),h=b.x,f=b.y-12):n&&(h=g.Cn(b,"ytp-miniplayer-button-top-left"),f=g.Lh(b,this.element),b=g.Oh(b),h?(h=8,f=f.y+40):(h=f.x-l.width+b.width,f=f.y-20))}else h=c-l.width/2,d=25+(e||0);b=g.QM(this.player).getPlayerSize().width;e=f+(e||0);l=g.Rd(h,0,b-l.width);e?(a.style.top=e+
"px",a.style.bottom=""):(a.style.top="",a.style.bottom=d+"px");a.style.left=l+"px"};
g.k.showControls=function(){};
g.k.Kh=function(){};
g.k.jh=function(){return!1};g.t(Q5,g.uN);Q5.prototype.create=function(){};
Q5.prototype.ag=function(){return!1};
Q5.prototype.load=function(){this.player.hideControls();this.o.show()};
Q5.prototype.unload=function(){this.player.showControls();this.o.hide()};g.FN.miniplayer=Q5;})(_yt_player);
