#!/usr/bin/perl -w
use lib '/tmp/mytools/pl/lib';
use threads; 
use Socket;
use Net::IP;
use Thread::Queue;
use Thread::Semaphore; 

# flush the print buffer immediately
$| = 1;
my $q = Thread::Queue-> new(); 

my $mutex = Thread::Semaphore->new( 1 );   #mutex

sub scan{
		local($target,$port)=@_;
	    $ip_a= sockaddr_in($port, inet_aton($target)); 
        $proto=getprotobyname('tcp');  
        socket(SOCK, PF_INET, SOCK_STREAM,$proto);
        if(connect(SOCK,$ip_a))
		{ 
             print "[#] host:$target:$port is Open! [#]\n";
   }
          close(SOCK);
}

sub worker { 
		my($target)=@_;
		while(1) { 
				$mutex ->down();
				my $r = $q->dequeue_nb();
				$mutex ->up();
				if ($r){
						&scan($target,$r)
				}
				else{
						last;
				} 
   } 
}

my @portlist;
if (index($ARGV[1],"-")>0){
		@rport=split(/-/,$ARGV[1]);
		for($port=$rport[0];$port<=$rport[1];$port++){
				push @portlist,$port;
		}
}
elsif (index($ARGV[1],",")>0){
		@portlist=split(/,/,$ARGV[1]);
}
else{
		push @portlist,$ARGV[1];
}

foreach $port (@portlist){
		$q->enqueue($port);
}


my $nb_process = 100;
if (@ARGV == 3){
		$nb_process = $ARGV[2];}
my $tn=0;
my @Threads;
while ($tn < $nb_process) {
 		my $thread = threads->create(\&worker, $ARGV[0]);
		push (@Threads, $thread);
		$tn = $tn+1;
		}
foreach my $thr (@Threads)
{
$thr->join;
}



#my $ip = new Net::IP ($ARGV[0]) or die (Net::IP::Error());
#my @iplist;
#do {
#   push @iplist, $ip->ip();
#} while (++$ip);
#print @iplist[10]
#&scan($ARGV[0],$ARGV[1]);

