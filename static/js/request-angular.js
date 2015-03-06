angular.module("myApp", ['ngRoute', 'ngCookies', 'infinite-scroll', 'ui.bootstrap']);

angular.module("myApp").run(['$http','$cookies', function($http, $cookies){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
}]);

angular.module("myApp").config(function($routeProvider){
    $routeProvider
        .when('/requests', {
            templateUrl: 'RequestsTablePage',
            controller: 'RequestsCtrl'
        })
        .when('/requests/form', {
            templateUrl: 'RequestPage',
            controller: 'RequestFormCtrl'
        })
        .when('/requests/form/:id', {
            templateUrl: 'RequestPage',
            controller: 'RequestFormCtrl'
        })
        .when('/performers', {
            templateUrl: 'PerformersPage',
            controller: 'PerformerCtrl'
        })
        .otherwise({
            redirectTo: '/requests'
        })
});

// Храним id редактируемой заявки при переходе на страницу редактирования
angular.module("myApp").factory('editedRequest', function(){
    return {
        id: null
    };
});

angular.module("myApp").factory('urls', function(){
    return {
        api_request_list : '/api/request_list',
        //api_request_list : '{% url 'api_request_list' %}',
        api_performer_list : '/api/performer_list/',
        api_detail_performer_list : '/api/detail_performer_list/'
        //api_performer_list : '{% url 'api_performer_list' %}'
    }
});

// Страницы для переходов
angular.module("myApp").factory('pages', function(){
    return {
        requestList : 'requestTable',
        requestDetail : 'requestForm',
        performers : 'performerForm'
    }
});

// формируем сообщение об ошибки для запросов
angular.module("myApp").factory('getErrorMessage', function(){
    return function(data, status, headers, config){
        if (status == 403){
            return data.detail
        }
        return data;
    }
});


angular.module("myApp").factory('globalFilters', function() {
    return {
        filters: {
            status:null,
            performer:null
        }
    }
});

function getNormalDate(date){
    try {
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        var todayFormat = year + '-' + (month > 9 ? '' : '0') + month + '-' + (day > 9 ? '' : '0') + day;
        return todayFormat
    }
    catch(ex) {
        return date
    }
    //return angular.$filter('date')(date,'yyyy-MM-dd');
    //return date.substring(0, date.indexOf('T'))
}


angular.module("myApp").directive('unique', ['$http', function($http) {
    return {
        require: 'ngModel',
        //compile: function CompilingFunction($templateElement, $templateAttributes) {
        //    return function LinkingFunction($scope, $linkElement, $linkAttributes, $constructor) {
        //        alert($constructor.$modelValue);
        //        //console.log($constructor);
        //        //console.log($scope.RequestForm.in_number)//.$modelValue);
        //    }
        //},
        link: function(scope, ele, attrs, constructor) {
            //var currentValue = constructor.$modelValue;
            //alert(constructor.$modelValue)
            //console.log(constructor);
            //ele.on('$focus', function(){
            //ele.bind('$focus', function(){
            var initValue = null;
            var focusFlag = false;
            //ele.on('focus', function(){ //+
            ele.bind('focus', function(){ //+
                focusFlag = true;
            });
            scope.$watch(attrs.ngModel, function() {


                if (constructor.$modelValue) {
                    if (!focusFlag){
                        initValue = constructor.$modelValue
                    }
                    if (initValue != constructor.$modelValue){
                        var params = attrs.unique.split('.');
                        //alert(constructor.$modelValue)
                        //console.log(constructor.$modelValue)
                        var req = {
                            method: 'POST',
                            url: '/api/check/',
                            data: {
                                model: params[0],
                                field: params[1],
                                value: constructor.$modelValue
                            }
                        };
                        //console.log(req);
                        $http(req)
                        .success(function (data, status, headers, cfg) {
                            //console.log(data);
                            //console.log(data.result);
                            constructor.$setValidity('unique', !data.result);
                        })
                        .error(function (data, status, headers, cfg) {
                        });
                    }
                }
                else{
                    constructor.$setValidity('unique', true);
                }
            });

        }
        //link: {
        //    pre: function PreLinkingFunction($scope, $element, $attributes, constructor) { alert(constructor.$modelValue) },
        //    post: function PostLinkingFunction($scope, $element, $attributes, constructor) { alert(constructor.$modelValue) }
        //}
    }
}]);

//angular.module("myApp").directive('myNormalDate',function(){
//    return function (scope, element, attrs) {
//        element.on('$change', function() {

        //element.on('click', al);

        //element.bind('$change', function(){
        //    alert('clk')
        //});
        //function al(){
        //    alert('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        //}
        //var date = scope[attrs["ngModel"]];
        //scope[attrs["ngModel"]] = getNormalDate(date)
        //$element.on('change', function(){
        //    alert('date chage')
        //});
        //if (angular.isArray(data.answers)) {
        //    var ulElem = angular.element("<ul>");
        //    element.append(ulElem);
        //    for (var i = 0; i < data.answers.length; i++) {
        //        var liElem = angular.element('<li>');
        //        liElem.append(angular.element('<p>').text(data.answers[i].text));
        //        ulElem.append(liElem);
        //    }
        //}
//    }
//});


angular.module("myApp").directive('myTest',function(){
    return {
        require: 'ngModel',
        link: function(scope, ele, attrs, c) {
            //return function(scope, element) {
            //$element.on('change',function() {
            scope.$watch(attrs.ngModel, function () {
                //    $element.datepicker();
                alert('test dirrective')
            });
            //$element.children().hide();
            //       $(this).children().toggle();
        }
    }
});

//######################################################################
//#################### Общий контроллер + навигация ####################
//######################################################################
angular.module("myApp").controller('BodyCtrl', function ($scope, $http, editedRequest, pages, getErrorMessage, urls) {
    //$scope.virtualPage = pages.requestList;
    //$scope.virtualPage = pages.requestDetail;
    $scope.virtualPage = pages.performers;

    $scope.redirect = function(page){
        $scope.virtualPage = page;
    };

    $scope.setRequestForm = function(){
        $scope.virtualPage = pages.requestDetail;
        // При переходе с редактируемой заметки на создание новой, очищаем форму
        $scope.$broadcast('clearForm');
    };

    $scope.testModelChange = function(param){
        alert($scope.testModel)
    };
});

//###############################################################################
//#################### Контроллер отображения таблицы заявок ####################
//###############################################################################
angular.module("myApp").controller('RequestsCtrl', function ($scope, $http, editedRequest, pages, getErrorMessage, urls, $location, globalFilters) {
    $scope.filters = globalFilters.filters;
    readyGetNextPage = true;
    ordering = null;
    nextPage = null;

    $scope.$on('$routeChangeStart', function(){
        globalFilters.filters = {
            status:null,
            performer:null
        };
    });

    // Формирование данных для GET запрос - фильтры, сортировка, страница
    var getParams = function(changed) {
        var params = {};
        if ($scope.filters) {

            //console.log('Filters : ');
            //console.log($scope.filters);
            //console.log('nextPage in filters : ');
            //console.log(nextPage);
            //if($scope.filters.filling_date){
            //    $scope.filters.filling_date = getNormalDate($scope.filters.filling_date)
            //}
            for (var filter in $scope.filters){
                if ($scope.filters[filter] == '' || $scope.filters[filter] == 'null'){
                    $scope.filters[filter] = null;
                }
            }
            params = JSON.stringify($scope.filters);
            params = JSON.parse(params);
            if(params.filling_date){
                params.filling_date = getNormalDate($scope.filters.filling_date)
            }
            if(params.performance_date){
                params.performance_date = getNormalDate($scope.filters.performance_date)
            }
        }
        // добавляем сортировку
        if (ordering){
            params.ordering = ordering;
        }
        // если нужна следующая страница добавляем номер страницы в параметры запроса,
        // в остальных случаях сбрасываем номер страницы.
        if (changed == 'page') {
            if (nextPage){
                page = nextPage.substring(nextPage.indexOf('page=')+5)
                if (page.indexOf('&') != -1){
                    params.page = page.substring(0,page.indexOf('&'))
                }
                else{
                    params.page = page;
                }
            }
        }
        else{
            params.nextPage = null;
            $scope.requests = [];
        }
        console.log('params : ')
        console.log(params)
        return params;
    };

    $scope.orderBy = function(field){
        // Определяем по какому полю сортировать.
        ordering = ordering == field ? '-' + field : field;
        $scope.getRequests('order');
    };

    // Получаем список всех исполнителей.
    $scope.getPerformerList = function(){
        $http.get(urls.api_performer_list)
            .success(function(data, status, headers, config) {
                $scope.performers = data.results;
                //$scope.filters.performer=null;
            })
            .error(function(data, status, headers, config ){
                $scope.error = getErrorMessage(status, headers, config, data)
            })
    };

    // При прокрутке подгружаем данные
    $scope.loadMore = function() {
        // Если следущей страницы нет, ничего не грузим
        if (!nextPage){
            return;
        }
        // Ждем пока не загрузим предыдущюю страницу
        if(readyGetNextPage) {
            readyGetNextPage = false;
            $scope.getRequests('page');
        }
    };

    // Получаем заявки
    $scope.getRequests = function(changed){
        $http.get(urls.api_request_list, {params: getParams(changed)})
            .success(function(data, status, headers, config) {
                $scope.requests = $scope.requests.concat(data.results);
                nextPage = data.next;
                readyGetNextPage = true;
                console.log('next Page : ');
                console.log(nextPage);
            })
            .error(function(data, status, headers, config ){
                $scope.error = getErrorMessage(data, status, headers, config);
            });
    };

    // Переходим к редактированию заявки.
    $scope.requestEdit = function(id){
        // Сохраняем id редактируемой заметки
        //editedRequest.id = id;
        $location.path("/requests/form/" + id);
        //$scope.location = $location;
        //$scope.redirect(pages.requestDetail);
    };

    // Разукрашиваем строки таблицы.
    $scope.rowClass = function(request){
        if(request.out_number){
            //return 'bg-success';
            return 'status_complete';
        }
        else{
            var curr_date = new Date().valueOf();
            var out_date = new Date(request.performance_date.replace(/(\d+)-(\d+)-(\d+)/, '$1/$2/$3')).valueOf();
            if(curr_date > out_date){
                //return 'bg-danger';
                return 'status_overdue';
            }
            else{
                //return 'bg-warning';
                return 'status_active';
            }
        }
    };
    $scope.getRequests('filter');
    //$scope.getPerformerList();
    //$scope.showDatepicker = function(){
    //    $( "#fInDate" ).datepicker();
    //}
});


//##########################################################################################
//####################  Контроллер формы Создания/редактирования заявки ####################
//##########################################################################################
angular.module("myApp").controller('RequestFormCtrl', function($scope, $http, editedRequest, pages, getErrorMessage, urls, $routeParams){
    // Получаем id заявки для редактирования
    //var id = editedRequest.id;
    //editedRequest.id = null;

    var id = $routeParams.id;
    // При переходе с редактируемой на создаваемую, очищаем форму
    //$scope.$on('clearForm', function(){
    //    $scope.request = null;
    //    $scope.error = null;
    //    $scope.selectedPerformer = null;
    //
    //    setDates();
    //
    //});

    // Получаем JSON с исполнителями
    getPerformerList = function(){
        $http.get(urls.api_performer_list)
            .success(function(data, status, headers, config) {
                $scope.performers = deleteDisabledPerformers(data.results);
            })
            .error(function(data, status, headers, config ){
                $scope.error = getErrorMessage(data, status, headers, config);
            });
    };

    if(id){
        // Получаем данные заявки для редактирования
        $http.get(urls.api_request_list + '/'+ id +'/')
            .success(function(data) {
                $scope.request = data;
                getPerformerList();
            })
            .error(function(data, status, headers, config ){
                $scope.error = getErrorMessage(data, status, headers, config);
            });
    }
    else{
        getPerformerList();
        // Устанавливаем сегодняшнюю входящую дату для новой заявки
        setDates();
        //setNextWeek();
    }
    // Создаем новую или редактируем старую заявку
    $scope.saveRequest = function(data, form) {
        if (form.$valid) {
            $scope.error = undefined;
            var req = {
                method : 'POST',
                url : urls.api_request_list
            };
            if ($scope.request.id){
                req.method = 'PUT';
                req.url = urls.api_request_list + '/'+ $scope.request.id +'/';
            }
            data.filling_date = getNormalDate(data.filling_date);
            data.performance_date = getNormalDate(data.performance_date);
            if (data.out_number == ''){
                data.out_number = null;
            }
            //data.performer = $scope.selectedPerformer.id
            req.data = data;
            $http(req)
                .success(function(data, status, headers, config){
                    //$scope.redirect(pages.requestList);
                })
                .error(function(data, status, headers, config ){
                    $scope.error = getErrorMessage(data, status, headers, config);
                });
        }
        else {
            $scope.error = 'Ошибка при заполнении полей';
        }
    };

    function deleteDisabledPerformers(performers){
        clearPerformers = [];
        for (var i=0; i<performers.length; i++){
            if (performers[i].active){
                clearPerformers.push(performers[i])
            }
        }
        return clearPerformers;
    }

    function setDates(){
        var week = 604800000;
        if (!$scope.request){
            $scope.request = {}
        }
        $scope.request.filling_date = getNormalDate(new Date());
        $scope.request.performance_date = getNormalDate(new Date(new Date().valueOf()+week));

    }
});

//#################################################################
//#################### Контроллер исполнителей ####################
//#################################################################
angular.module("myApp").controller('PerformerCtrl', function($scope, $http, getErrorMessage, urls, globalFilters, $location){
    //$scope.globalFilters = globalFilters;
    // Получаем JSON с исполнителями
    getPerformerList = function(){
        $http.get(urls.api_detail_performer_list)
            .success(function(data, status, headers, config) {
                $scope.performers = data.results;
                getSummaryInfo($scope.performers);
            })
            .error(function(data, status, headers, config ){
                $scope.error = getErrorMessage(data, status, headers, config);
            });
    };

    $scope.save = function(data, form){
        if (form.$valid){
            $http.post(urls.api_performer_list, {"name": data})
                .success(function(data){
                    getPerformerList();
                    $scope.newPerformerName = null;
                })
                .error(function(data, status, headers, config ){
                    $scope.error = getErrorMessage(data, status, headers, config);
                });
        }
    };

    $scope.editPerformer = function(performer){
        $http.put(urls.api_performer_list + performer.id + '/', performer)
            .success(function(data){
                getPerformerList();
            })
            .error(function(data, status, headers, config ){
                $scope.error = getErrorMessage(data, status, headers, config);
            });
    };

    function getSummaryInfo(performers){
        for (var i=0; i<performers.length; i++) {
            var performer = performers[i];
            performer.completeCount = 0;
            performer.activeCount = 0;
            performer.overdueCount = 0;
            for (var j = 0; j < performer.requests.length; j++) {
                var request = performer.requests[j];
                if (request.out_number) {
                    performer.completeCount++;
                }
                else {
                    var curr_date = new Date().valueOf();
                    var out_date = new Date(request.performance_date.replace(/(\d+)-(\d+)-(\d+)/, '$1/$2/$3')).valueOf();
                    if (curr_date > out_date) {
                        performer.overdueCount++;
                    }
                    else {
                        performer.activeCount++;
                    }
                }
            }
        }
    }

    $scope.gotoRequests = function(filter){
        //$scope.error = filter;
        globalFilters.filters = filter;
        $location.path("/requests");
    };

    getPerformerList();
});