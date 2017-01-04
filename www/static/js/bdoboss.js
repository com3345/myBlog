$(function() {
    new Clipboard('.btn');
    var themecolorlist = [
        ["linear-gradient(to right, #ccccff 0%, #ff99cc 100%)","rgba(255, 153, 204, 0.05)", "rgba(255, 153, 204, 0.85)"],
        ["linear-gradient(to right, #99ff33 0%, #66ccff 100%)", "rgba(102, 204, 255, 0.05)", "rgba(102, 204, 255, 0.85)"],
        ["linear-gradient(to right, #ff9900 0%, #ff0000 100%)", "rgba(255, 0, 0, 0.05)", "rgba(255, 0, 0, 0.85)"],
        ["rgb(84, 132, 164)", "rgba(84, 132, 164, 0.05)", "rgb(84, 132, 164, 0.85)"],
        ["rgb(246, 209, 85)", "rgba(246, 209, 85, 0.05)", "rgba(246, 209, 85, 0.85)"],
        ["rgb(0, 75, 141)", "rgba(0, 75, 141, 0.05)", "rgba(0, 75, 141, 0.85)"],
        ["rgb(242, 85, 44)", "rgba(242, 85, 44, 0.05)", "rgba(242, 85, 44, 0.85)"],
        ["rgb(149, 222, 227)", "rgba(149, 222, 227, 0.05)", "rgba(149, 222, 227, 0.85)"],
        ["rgb(237, 205, 194)", "rgba(237, 205, 194, 0.05)", "rgba(237, 205, 194, 0.85)"],
        ["rgb(136, 176, 75)", "rgba(136, 176, 75, 0.05)", "rgba(136, 176, 75, 0.85)"],
        ["rgb(206, 49, 117)", "rgba(206, 49, 117, 0.05)", "rgba(206, 49, 117, 0.85)"],
        ["rgb(90, 114, 71)", "rgba(90, 114, 71, 0.05)", "rgba(90, 114, 71, 0.85)"],
        ["rgb(207, 176, 149)", "rgba(207, 176, 149, 0.05)", "rgba(207, 176, 149, 0.85)"]
    ];
    var sitesList = [
        'http://heeeeeeeey.com/',
        'http://thatsthefinger.com/',
        'http://cant-not-tweet-this.com/',
        'http://weirdorconfusing.com/',
        'http://eelslap.com/',
        'http://www.staggeringbeauty.com/',
        'http://burymewithmymoney.com/',
        'http://endless.horse/',
        'http://www.fallingfalling.com/',
        'http://just-shower-thoughts.tumblr.com/',
        'http://ducksarethebest.com/',
        'http://www.trypap.com/',
        'http://www.republiquedesmangues.fr/',
        'http://www.movenowthinklater.com/',
        'http://www.partridgegetslucky.com/',
        'http://www.rrrgggbbb.com/',
        'http://beesbeesbees.com/',
        'http://www.sanger.dk/',
        'http://www.koalastothemax.com/',
        'http://www.everydayim.com/',
        'http://www.leduchamp.com/',
        'http://www.haneke.net/',
        'http://r33b.net/',
        'http://randomcolour.com/',
        'http://cat-bounce.com/',
        'http://www.sadforjapan.com/',
        'http://www.taghua.com/',
        'http://chrismckenzie.com/',
        'http://hasthelargehadroncolliderdestroyedtheworldyet.com/',
        'http://ninjaflex.com/',
        'http://iloveyoulikeafatladylovesapples.com/',
        'http://ihasabucket.com/',
        'http://corndogoncorndog.com/',
        'http://www.ringingtelephone.com/',
        'http://www.pointerpointer.com/',
        'http://imaninja.com/',
        'http://willthefuturebeaweso.me/',
        'http://www.ismycomputeron.com/',
        'http://www.nullingthevoid.com/',
        'http://www.muchbetterthanthis.com/',
        'http://www.ouaismaisbon.ch/',
        'http://www.yesnoif.com/',
        'http://iamawesome.com/',
        'http://www.pleaselike.com/',
        'http://crouton.net/',
        'http://corgiorgy.com/',
        'http://www.electricboogiewoogie.com/',
        'http://www.wutdafuk.com/',
        'http://unicodesnowmanforyou.com/',
        'http://www.crossdivisions.com/',
        'http://tencents.info/',
        'http://intotime.com/',
        'http://leekspin.com/',
        'http://minecraftstal.com/',
        'http://www.patience-is-a-virtue.org/',
        'http://whitetrash.nl/',
        'http://www.theendofreason.com/',
        'http://zombo.com',
        'http://pixelsfighting.com/',
        'http://baconsizzling.com/',
        'http://isitwhite.com/',
        'http://onemillionlols.com/',
        'http://www.omfgdogs.com/',
        'http://oct82.com/',
        'http://semanticresponsiveillustration.com/',
        'http://chihuahuaspin.com/',
        'http://potato.io/',
        'http://www.blankwindows.com/',
        'http://www.biglongnow.com/',
        'http://dogs.are.the.most.moe/',
        'http://tunnelsnakes.com/',
        'http://www.infinitething.com/',
        'http://www.trashloop.com/',
        'http://www.ascii-middle-finger.com/',
        'http://www.coloursquares.com/',
        'https://annoying.dog/',
        'http://spaceis.cool/',
        'https://thebigdog.club/'
    ];
    var vm = new Vue({
        el: '#vm',
        data: {
            timerforautorefresh: 0,
            timerforrefreshbutton: 20,
            bossinfoloading: true,
            presentcodeloading: true,
            now: new Date(),
            codeslidenumber: 0,
            copied_codeslice: '',
            search_query: '',
            random_link: '',
            bdnow: [],
            loadingjoke: '',
            nextnight: 0,
            leftnight: 0,
            bosses: {
                nube: [],
                kutu: [],
                kuza: [],
                kara: []
            },
            presentcodes: [],
        },
        mounted: function (){
            this.readpresentcodes();

            this.get_joke();
            this.refreshbossinfo();
            // this.refreshpresentcode();
            
            setInterval(this.clock, 1000)
        },
        computed: {
            themecolor: function () {
                return themecolorlist[Math.floor(Math.random() * themecolorlist.length)]
            },

            night: function () {
                var res = true;
                var timez_shift_to_Jp = 9 + this.now.getTimezoneOffset() / 60;
                var now_h = this.now.getHours() + timez_shift_to_Jp ;

                var now_m = this.now.getMinutes();
                var minutes = now_h * 60 + now_m;  // 0 ~ 1440 从现实世界0点开始到现在的分钟数

                if (minutes > 0 && minutes <= 40) {
                    // 白天 现实世界0点～0:40的游戏白天
                    res = false;
                    this.nextnight = 40 - minutes
                    this.bdnow[0] = float2int(((160 + minutes) * 4.5) / 60) + 7;
                    this.bdnow[1] = float2int(((160 + minutes) * 4.5) % 60);
                } else if (minutes > 1280 && minutes <= 1440) {
                    // 白天 现实世界21:20~0点的游戏白天
                    res = false;
                    this.nextnight = 1480 - minutes;
                    this.bdnow[0] = float2int(((minutes - 1280) * 4.5) / 60) + 7;
                    this.bdnow[1] = float2int(((minutes - 1280) * 4.5) % 60);

                } else {
                    // alert(minutes);
                    var rem = (minutes - 40) % 240; // 超过游戏每个夜昼循环循环开始的真实世界分钟数

                    if (rem >= 40 ) {
                        // 白天
                        res = false;
                        this.nextnight = 240 - rem;
                        this.bdnow[0] = float2int(((rem - 40)* 4.5) / 60) + 7; // 7点开始算
                        this.bdnow[1] = float2int(((rem - 40)* 4.5) % 60);

                    } else {
                        // 夜里
                        res = true;
                        this.nextnight = 0;
                        this.nightleft = 40 - rem;
                        this.bdnow[0] = float2int(((rem) * 13.5) / 60) + 22; // 22点开始算
                        if (this.bdnow[0] >= 24) {
                            this.bdnow[0] -= 24
                        }
                        this.bdnow[1] = float2int(((rem) * 13.5) % 60);
                    }
                }
                return res
            },
            timezonestring: function () { 
                var timezoneoffset = this.now.getTimezoneOffset() / 60 ;
                var timezone = '';
                if (timezoneoffset == -9) {
                    timezone = '东京时间'
                } else if (timezoneoffset == -8) {
                    timezone = '北京时间'
                } else if (timezone >= 0) {
                    timezone = timezoneoffset.toString() + '时区时间'
                } else {
                    timezone = (- timezoneoffset).toString() + '时区时间'
                }
                return timezone
            },

            data2clipboard: function () {
                var text = '';

                text += '以下皆为 ' + this.timezonestring + '\n';
                text += '[龙]:上次 ' + this.bosses.nube[4] + ', 预计' + this.bosses.nube[5] + '\n';
                text += '[虫]:上次 ' + this.bosses.kutu[4] + ', 预计' + this.bosses.kutu[5] + '\n';
                text += '[库]:上次 ' + this.bosses.kuza[4] + ', 预计' + this.bosses.kuza[5] + '\n';
                text += '[鸟]:上次 ' + this.bosses.kara[4] + ', 预计' + this.bosses.kara[5] + '\n';
                text += 'Ps:(预计)指本次最早可能出现的时间\n';
                // text += '游戏夜晚信息:'
                if (this.nextnight > 0) {
                    text += '距游戏内夜晚 降临 还有' + this.nextnight.toString() + '分钟.';
                } else {
                    text += '离游戏内夜晚 结束 还有' + this.nightleft.toString() + '分钟';
                }
                text += '\n该信息由黑色沙漠天气预报系统提供\n访问http://hazydawn.com/bdo_boss';

                return text
            },
        },



        methods: {
            set_search_query: function (e) {
                this.search_query = "http://www.baidu.com/s?wd=" + e.target.innerText
            },

            set_copied_codeslice: function (e) {
                var codeslice = e.target.innerText
                alert(codeslice + " 已拷贝！")
                this.copied_codeslice = codeslice
            },

            set_random_link: function() {
                var idx = Math.floor(Math.random() * sitesList.length);
                this.random_link = sitesList[idx];
                sitesList.splice(idx, 1);
            },

            cal_codeslidenumber: function () {
                if (this.codeslidenumber >= this.presentcodes.length - 1) {
                    this.codeslidenumber = 0
                } else {
                    this.codeslidenumber += 1
                }
            },            
            refreshbossinfo: function() {
                    this.get_joke();
                    this.bossinfoloading = true;
                    this.timerforautorefresh = 0;
                    this.timerforrefreshbutton = 20;
                    getJSON('/api/crawl_boss', 
                    function(err, result) {
                    if (err) {
                        alert('ERROR: Refresh too often!');
                    }
                    else {
                        vm.bosses.nube = result.nube;
                        vm.bosses.kutu = result.kutu;
                        vm.bosses.kuza = result.kuza;
                        vm.bosses.kara = result.kara;

                        vm.bossinfoloading = false;
                        for (b in vm.bosses) {
                            format_time(vm.bosses[b]);
                        }
                    }
                    });

            },
            // refreshpresentcodes: function () {
            //     this.presentcodeloading = true;

            //     getJSON('/api/get_presentcode', 
            //         function(err, result) {
            //             if (err) {
            //                 alert("ERROR: 获取礼物代码失败！")
            //             } else {
            //                 vm.presentcodes = result;
            //                 }
            //             }

            //     );
            // },
            readpresentcodes: function () {
                $.ajax({
                    url: "/static/presentcodes.json",
                    success: function (data) {
                        vm.presentcodes = data;
                    }
                });

            },

            get_joke: function () {
                    getJSON('/api/get_joke',
                    function (err, result) {
                        
                        if (err) {
                            alert('ERROR:我们没有笑话了！');
                        } else {
                            if (result.joke.indexOf('$$$') > -1 ) {
                                vm.loadingjoke = result.joke.split()
                            }
                            vm.loadingjoke = result.joke;
                        }
                    });
            },

            clock: function() {
                this.now = new Date();
                this.timerforautorefresh += 1;
                this.timerforrefreshbutton -= 1;
                if (this.timerforautorefresh > 60) {

                    this.refreshbossinfo()
                }
            },
            probability: function(boss) {

                nextdate = str2time(boss[2]);
                var prob = '';

                if (vm.now < nextdate) {

                    prob = 0
                } else {
                    prob = (this.now - nextdate) / (3600 * boss[3] * 1000) * 100
                }
                return prob
            },
            bosscolor: function(prob) {
                var c = '';
                if (prob < 25 && prob > 0) {
                    c = 'uk-text-primary'
                } else if (prob < 50 && prob >= 25) {
                    c = 'uk-text-success'
                } else if (prob < 75 && prob >= 50) {
                    c = 'uk-text-warning'
                } else if (prob >= 75) {
                    c = 'uk-text-danger'
                }
                return c
            },
            whichdialog: function (index) {
                return "#modal" + index.toString()
            },
        },
    });
});



function format_time(boss){
    var lastdate = str2time(boss[1]);
    var nextdate = str2time(boss[2]);
    var l_nextdate = nextdate.getHours() + nextdate.getMinutes() / 60 + boss[3];

    boss.push(whichday(lastdate) + ' ' + time2hourminute(lastdate));

    if (nextdate.getDay() == 3 && l_nextdate > 8.5 ) {    
        boss.push('周三维护作息紊乱')
    } else {
        boss.push(whichday(nextdate) + ' ' + time2hourminute(nextdate));
    }
    boss.push(0)
}

function whichday(time) {
    var now = new Date();
    var now_day = now.getDate();
    var time_day = time.getDate();
    var now_year = now.getFullYear();
    var time_year = now.getFullYear();
    if (now_day == time_day) {
        return '今天'
    } else if (now_year == time_year) {
        if (now_day < time_day) {
            return '明天'
        } else {
            return '昨天'
        }
    } else if (now_year < time_year) {
        return '明天'
    } else {
        return '昨天'
    }
}

function str2time(t) {
    return new Date(t * 1000)
}

function time2hourminute(t) {
    return t.toTimeString().split(' ')[0].slice(0, 5)
}

function float2int(f) {
    return f | 0
}

