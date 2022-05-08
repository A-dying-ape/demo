/**
 * @Description: Wechat 8015 hook script
 * @author XQE
 * @date 2022/04/19
*/


var tools = {
    classexists: function (className) {
        var _exists = false
        try {
            Java.use(className)
            _exists = true
        } catch (err) {
        }
        return _exists
    },

    checkloaddex: function (className, dexfile) {
        if (!this.classexists(className)) {
            Java.openClassFile(dexfile).load()
        }
    },

    tojsonstring: function (obj) {
        try {
            this.checkloaddex("com.alibaba.fastjson.JSON", "/data/local/tmp/fastjson.dex")
            var _clz = Java.use("com.alibaba.fastjson.JSON")
            var _toJSONStringMehtod = _clz.toJSONString.overload("java.lang.Object")
            return _toJSONStringMehtod.call(_clz, obj)
        } catch (err) {
            console.log(err)
        }
        return "{}"
    },

    fromjsonstring: function (jsonStr, classObj = null) {
        try {
            this.checkloaddex("com.alibaba.fastjson.JSON", "/data/local/tmp/fastjson.dex")
            if (classObj == null) {
                var _clz = Java.use("com.alibaba.fastjson.JSON")
                return _clz.parseObject(jsonStr)
            } else {
                var _jsonObject = Java.use("com.alibaba.fastjson.JSONObject")
                var _obj = _jsonObject.parseObject(jsonStr, classObj.class)
                return _obj
            }
        } catch (err) {
            console.log(err)
        }
        return null
    },

    recursionremove: function (jsonObject, removeKey) {
        var _keyArray = jsonObject.keySet().toArray()
        for (var i = 0; i < _keyArray.length; i++) {
            var _key = _keyArray[i]
            var _object = jsonObject.get(_key)
            var _objectType = ""
            try {
                _objectType = _object.getClass().getName()
            } catch (e) {}
            if (_key == removeKey && _objectType == "java.lang.String") {
                jsonObject.remove(_key)
            }
            if (_objectType == "com.alibaba.fastjson.JSONObject") {
                this.recursionremove(jsonObject.getJSONObject(_key), removeKey)
            }
            if (_objectType == "com.alibaba.fastjson.JSONArray") {
                var jsonArray = jsonObject.getJSONArray(_key)
                for (var a = 0; a <= jsonArray.size(); a++) {
                    try {
                        var _childObj = jsonArray.getJSONObject(a)
                        if (_childObj) {
                            this.recursionremove(_childObj, removeKey)
                        }
                    } catch (e) {
                        console.log(e)
                    }
                }
            }
        }
    },

    wxhelper: function () {
        try {
            this.checkloaddex("com.alibaba.fastjson.JSON", "/data/local/tmp/fastjson.dex")
            this.checkloaddex("com.tencent.mm.wechathelperdex.WxHelper", "/data/local/tmp/wxhelper.dex")
            var _clz = Java.use("com.tencent.mm.wechathelperdex.WxHelper")
            return _clz
        } catch (err) {
            console.log(err)
        }
        return "{}"
    },

    hashset: function () {
        var _HashSetClz = Java.use("java.util.HashSet")
        var _hashset = _HashSetClz.$new()
        return _hashset
    },

    map: function () {
        var _hashMap_clz = Java.use("java.util.HashMap")
        var _map_clz = Java.use("java.util.Map")
        var _hashMap = _hashMap_clz.$new()
        var _map = Java.cast(_hashMap, _map_clz)
        return _map
    },

    base64: function (zsBase64) {
        var androidBase64 = Java.use("android.util.Base64")
        var _base64 = androidBase64.decode(zsBase64, 0)
        return _base64
    },
}

var hooker_fun = {
    runComment: function (device, reply, args) {},

    runDetailVideo: function (device, args) {},

    runDetailGoods: function (device, args) {},

    runLiveInfo: function (device, username, args) {},

    runLiveBarrage: function (device, username, args) {},
	
	runLiveContribution: function(device, username, args) {},

    runLiveGoods: function (device, username, args) {},

    runLiveSquare: function (device, cate) {},

    runLiveTab: function () {},

    runLiveBag: function (device, args) {},

    runProductList: function (device, selfappid, args) {},

    runProductInfo: function (device, selfappid, args) {},

    runProductStore: function (device, selfappid, args) {},

    runProductTakecenter: function (device, selfappid, cookie, args) {}

    runProductThird: function (device, selfappid, cookie, args) {},

    runGetcookie: function (device, username) {},

    runTopicTopic: function (device, args) {},

    runTopicActivity: function (device, tab, args) {},

    runVideoGoods: function (device, args) {},
    
    runVideoUrl: function (device, args) {},
}

rpc.exports = {
    hookerVideoComment: function (device, reply, args) {
        Java.perform(function () {
            hooker_fun.runComment(device, reply, args)
        })
    },

    hookerDetailVideo: function (device, args) {
        Java.perform(function () {
            hooker_fun.runDetailVideo(device, args)
        })
    },

    hookerDetailGoods: function (device, args) {
        Java.perform(function () {
            hooker_fun.runDetailGoods(device, args)
        })
    },

    hookerLiveInfo: function (device, username, args) {
        Java.perform(function () {
            hooker_fun.runLiveInfo(device, username, args)
        })
    },

    hookerLiveBarrage: function (device, username, args) {
        Java.perform(function () {
            hooker_fun.runLiveBarrage(device, username, args)
        })
    },

    hookerLiveContribution: function (device, username, args) {
        Java.perform(function () {
            hooker_fun.runLiveContribution(device, username, args)
        })
    },

    hookerLiveGoods: function (device, username, args) {
        Java.perform(function () {
            hooker_fun.runLiveGoods(device, username, args)
        })
    },

    hookerLiveSquare: function (device, cate) {
        Java.perform(function () {
            hooker_fun.runLiveSquare(device, cate)
        })
    },

    hookerLiveTab: function () {
        Java.perform(function () {
            hooker_fun.runLiveTab()
        })
    },

    hookerLiveBag: function (device, args) {
        Java.perform(function () {
            hooker_fun.runLiveBag(device, args)
        })
    },

    hookerProductList: function (device, selfappid, args) {
        Java.perform(function () {
            hooker_fun.runProductList(device, selfappid, args)
        })
    },

    hookerProductInfo: function (device, selfappid, args) {
        Java.perform(function () {
            hooker_fun.runProductInfo(device, selfappid, args)
        })
    },

    hookerProductStore: function (device, selfappid, args) {
        Java.perform(function () {
            hooker_fun.runProductStore(device, selfappid, args)
        })
    },

    hookerProductTakecenter: function (device, selfappid, cookie, args) {
        Java.perform(function () {
            hooker_fun.runProductTakecenter(device, selfappid, cookie, args)
        })
    },

    hookerProductThird: function (device, selfappid, cookie, args) {
        Java.perform(function () {
            hooker_fun.runProductThird(device, selfappid, cookie, args)
        })
    },

    hookerGetcookie: function (device, username) {
        Java.perform(function () {
            hooker_fun.runGetcookie(device, username)
        })
    },

    hookerTopicTopic: function (device, args) {
        Java.perform(function () {
            hooker_fun.runTopicTopic(device, args)
        })
    },

    hookerTopicActivity: function (device, tab, args) {
        Java.perform(function () {
            hooker_fun.runTopicActivity(device, tab, args)
        })
    },

    hookerVideoGoods: function (device, args) {
        Java.perform(function () {
            hooker_fun.runVideoGoods(device, args)
        })
    },

    hookerVersionCheck: function () {
        Java.perform(function () {
            hooker_fun.runVersionCheck()
        })
    },

    hookerVideoUrl: function (device, args) {
        Java.perform(function () {
            hooker_fun.runVideoUrl(device, args)
        })
    },
}
