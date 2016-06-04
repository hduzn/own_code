<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>我的旅行足迹</title>
<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=CwL0Aob6vtA1b1rwVOosPgLK">
</script>
<style type="text/css">
html{height:100%} 
body{height:100%;margin:0px;padding:0px}
#container{height:100%}
</style>
</head>
<body>
<div id="container"></div>

<script type="text/javascript">
//百度地图API
//http://lbsyun.baidu.com/index.php?title=jspopular/guide/helloworld
var map = new BMap.Map("container");
map.centerAndZoom(new BMap.Point(106.403765, 33.914850), 5); //116.403765, 39.914850
map.addControl(new BMap.NavigationControl({type: BMAP_NAVIGATION_CONTROL_SMALL}));
map.enableScrollWheelZoom(true);
//map.setMapStyle({style:'grayscale'});
var myStyleJson=[
          {
                    "featureType": "all",
                    "elementType": "all",
                    "stylers": {
                              "lightness": 10,
                              "saturation": -100
                    }
          }
];
map.setMapStyle({styleJson: myStyleJson });

var provinces = ["广西", "广东", "湖南", "贵州", "云南", "福建", "江西", "浙江", "安徽", "湖北", "河南", 
        "江苏", "四川", "海南", "山东", "辽宁", "新疆", "西藏", "陕西", "河北", "黑龙江", "宁夏", "台湾",
        "内蒙古自治区", "青海", "甘肃", "山西", "吉林", "北京", "天津", "上海", "重庆", "香港", "澳门"
    ];
var provinces1 = ["福建", "浙江", "江苏", "海南",  "上海", "陕西"];
var citys = new Array();
citys["福建省"] = "厦门市";
citys["海南省"] = "三亚市";
citys["陕西省"] = "西安市";
citys["上海市"] = "上海市";
citys["浙江省"] = "嘉兴市，杭州市，宁波市，绍兴市，诸暨市，乐清市";
citys["江苏省"] = "南京市，苏州市";

getAllBoundary(provinces, "#8c8c89");
getBoundary(provinces1, "#67adf4");

function getAllBoundary(provinces,color){       
    var bdary = new BMap.Boundary();
    map.clearOverlays();        //清除地图覆盖物
    for (var j = 0; j < provinces.length; j++) {
        bdary.get(provinces[j], function(rs){       //获取行政区域    
            var count = rs.boundaries.length; //行政区域的点有多少个
            for(var i = 0; i < count; i++){
                //建立多边形覆盖物
                var ply = new BMap.Polygon(rs.boundaries[i], {strokeWeight: 2, strokeColor: color}); 
                map.addOverlay(ply);  //添加覆盖物
                ply.addEventListener("click", function (e) {
                    var latlng = e.point;
                    var myGeo=new BMap.Geocoder();
                    myGeo.getLocation(new BMap.Point(e.point.lng,e.point.lat),function(result){
                        var info = new BMap.InfoWindow((result.addressComponents.province), {width:220});
                        map.openInfoWindow(info, latlng);
                    });
                });
            }                
        }); 
    }
}

function getBoundary(provinces,color){       
    var bdary = new BMap.Boundary();
    //map.clearOverlays();        //清除地图覆盖物
    for (var j = 0; j < provinces.length; j++) {
        bdary.get(provinces[j], function(rs){       //获取行政区域    
            var count = rs.boundaries.length; //行政区域的点有多少个
            for(var i = 0; i < count; i++){
                //Polygon类
                //http://developer.baidu.com/map/reference/index.php?title=Class:%E8%A6%86%E7%9B%96%E7%89%A9%E7%B1%BB/Polygon
                //建立多边形覆盖物
                var ply = new BMap.Polygon(rs.boundaries[i], {strokeWeight: 2, strokeColor: color, fillColor:color}); 
                map.addOverlay(ply);  //添加覆盖物
                //map.setViewport(ply.getPath());    //调整视野 
                ply.addEventListener("click", function (e) {
                    var latlng = e.point;
                    var myGeo=new BMap.Geocoder();
                    myGeo.getLocation(new BMap.Point(e.point.lng,e.point.lat),function(result){
                        var info = new BMap.InfoWindow((result.addressComponents.province+"："+window.citys[result.addressComponents.province]), {width:220});
                        map.openInfoWindow(info, latlng);
                    });
                    //var info = new BMap.InfoWindow(name + " " + latlng.lat + "," + latlng.lng, {width:220});
                    //map.openInfoWindow(info, latlng);
                    //高亮闪烁显示鼠标点击的省
                    /*delay = 0;
                    for (flashTimes = 0; flashTimes < 3; flashTimes++) {
                        delay += 200;
                        setTimeout(function () {
                            ply.setFillColor("#FFFF00");
                        }, delay);
                         
                        delay += 200;
                        setTimeout(function () {
                            ply.setFillColor(color);
                        }, delay);
                    }*/
                });
            }                
        }); 
    }
}

</script>
</body>
</html>