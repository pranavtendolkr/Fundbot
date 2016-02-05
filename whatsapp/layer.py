from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity

import subprocess as sub
import tradeoff
import dialog
import grapher

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        # send receipt otherwise we keep receiving the same message over and over

        if True:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
            message=messageProtocolEntity.getBody()
            print message + "\n"
            output,client_id = dialog.converse( messageProtocolEntity.getFrom(),message)
            print "=================================================client id=%s=========="%(str(client_id))
#	    profile = {}
#	    if "Is that correct?" in output:
#		print "in correct"
#		global profile
#		profile = dialog.get_profile(client_id)
#                print profile
#            if output == "Okay, thank you for using the service!":
            if "start over" in output or "another request" in output:
                profile = dialog.get_profile(client_id)
		print profile
                response,profile_has_graph = tradeoff.call_tradeoff_api(profile)
		print profile_has_graph
		import json
		with open('dump.json','w') as f:
		    json.dump(response,f)
                link=''		                
		if(profile_has_graph ==  True):
                    link = grapher.PlotGraph.plot_graph(response)
     		    print link
		# yes this line works. :P
                top5 = grapher.PlotGraph.top_five(response)
		print top5
                output = "The top mutual funds we selected for you are:\n"
                for i,item in enumerate(top5):
                    output = output + '%i,%s\n'%(i,item)
                output = (output + "\n Here is your graph: %s"%(link))if profile_has_graph else output 

            print output
            #output=message
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(output,
                to = messageProtocolEntity.getFrom())

            self.toLower(receipt)
            self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)
