angular.module("myApp", ['ngRoute', 'ngCookies', 'infinite-scroll']);

angular.module("myApp").run(['$http','$cookies', function($http, $cookies)
{
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
}]);

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
        api_performer_list : '/api/performer_list/'
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




//-------------------- Общий контроллер + навигация --------------------
angular.module("myApp").controller('BodyCtrl', function ($scope, $http, editedRequest, pages, getErrorMessage, urls) {
    $scope.virtualPage = pages.requestList;

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


//-------------------- Контроллер отображения таблицы заявок --------------------
angular.module("myApp").controller('RequestsCtrl', function ($scope, $http, editedRequest, pages, getErrorMessage, urls) {
    readyGetNextPage = true;
    ordering = null;
    nextPage = null;

    // Формирование данных для GET запрос - фильтры, сортировка, страница
    var getParams = function(changed) {
        var params = {};
        if ($scope.filters) {
            params = JSON.stringify($scope.filters);
            params = JSON.parse(params);
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
                $scope.performers = data;
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
            })
            .error(function(data, status, headers, config ){
                $scope.error = getErrorMessage(data, status, headers, config);
            });
    };

    // Переходим к редактированию заявки.
    $scope.requestEdit = function(id){
        // Сохраняем id редактируемой заметки
        editedRequest.id = id;
        $scope.redirect(pages.requestDetail);
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
    $scope.getRequests();
});


//--------------------  Контроллер формы Создания/редактирования заявки --------------------
angular.module("myApp").controller('RequestFormCtrl', function($scope, $http, editedRequest, pages, getErrorMessage, urls){
    // Получаем id заявки для редактирования
    var id = editedRequest.id;
    editedRequest.id = null;
    // При переходе с редактируемой на создаваемую, очищаем форму
    $scope.$on('clearForm', function(){
        $scope.request = null;
        $scope.selectedPerformer = null;
        setToday();
    });

    // Получаем JSON с исполнителями
    getPerformerList = function(){
        $http.get(urls.api_performer_list)
            .success(function(data, status, headers, config) {
                $scope.performers = data;
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
        setToday();
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
            if (data.out_number == ''){
                data.out_number = null;
            }
            //data.performer = $scope.selectedPerformer.id
            req.data = data;
            $http(req)
                .success(function(data, status, headers, config){
                    $scope.redirect(pages.requestList);
                })
                .error(function(data, status, headers, config ){
                    $scope.error = getErrorMessage(data, status, headers, config);
                });
        }
        else {
            $scope.error = 'Ошибка при заполнении полей';
        }
    };


    function setToday(){
        var today = new Date();
        var day = today.getDate();
        var month = today.getMonth() + 1;
        var year = today.getFullYear();
        var todayFormat =  year + '-' + (month > 10 ? '' : '0') + month + '-' + (day > 10 ? '' : '0') + day;
        $scope.request = { filling_date : todayFormat };
    }
});

//-------------------- Контроллер исполнителей --------------------
angular.module("myApp").controller('PerformerCtrl', function($scope, $http, getErrorMessage, urls){
    $scope.save = function(data, form){
        if (form.$valid){
            $http.post(urls.api_performer_list, {"name": data})
                .success(function(data){})
                .error(function(data, status, headers, config ){
                    $scope.error = getErrorMessage(data, status, headers, config);
                });
        }
    };
});