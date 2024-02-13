package com.cra.service;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import javax.mail.Part;
import javax.mail.internet.MimeBodyPart;
import org.springframework.stereotype.Service;

import com.entrust.toolkit.User;
import iaik.smime.SMimeEncrypted;
import iaik.smime.SMimeSigned;
import iaik.smime.SMimeCompressed;
import iaik.asn1.DerInputStream;
import iaik.asn1.SEQUENCE;
import iaik.asn1.CON_SPEC;
import iaik.asn1.OCTET_STRING;

@Service
public class DecryptService {

    public String decrypt(User user, byte[] data) throws Exception {
        InputStream inputStream = new ByteArrayInputStream(data);
        SMimeEncrypted sMimeEncrypted = new SMimeEncrypted(inputStream);
        sMimeEncrypted.decryptSymmetricKey(user);

        Part p = (Part) new MimeBodyPart(sMimeEncrypted.getInputStream());
        InputStream contentStream = (InputStream) p.getContent();
        
        // the line below reads the signature part from the message into a SMimeSigned object:
        SMimeSigned signed = new SMimeSigned(contentStream);
        //todo: see if there are signers using "signed.getSignerInfos().length"; if so, check the signature

        // now we take the unread part of content:
        Part q = (Part) new MimeBodyPart(contentStream);
        InputStream refinedContentStream = (InputStream) q.getContent();

        DerInputStream dis = new DerInputStream(refinedContentStream);
        // next tag may be 4, meaning octet string
        // after that is 16, which means sequence
        // after that is 6, which means object id
        // after that is 0, which means we've reached the end
        // let's read the sequence, which is of type CMS compressedData
        // to do so, we have to read the octet string first, if present:
        if (dis.nextTag() == 4) {
            dis.readOctetString();
        }
            
        // SMimeCompressed reads from dis where we left off, which is the sequence
        SMimeCompressed sMimeCompressed = new SMimeCompressed(dis);

        // if we write SMimeCompressed to a file right now, we get the headers at the top, e.g.:
        // MIME-Version: 1.0
        // Content-Type: text/plain;
        // 	charset="US-ASCII";
        // 	name=ABCVR00085
        // Content-Transfer-Encoding: 7bit
        // Content-Disposition: attachment;
        // 	filename=ABCVR00085

        // have to find a way to remove this...
        // try:

        // calling toASN1Object decompresses the data (I think...)
        SEQUENCE sequence = (SEQUENCE) sMimeCompressed.toASN1Object();
        // there are 2 components
        // the first component is an object id, second is con_spec:
        CON_SPEC a = (CON_SPEC) sequence.getComponentAt(1);
        // a has exactly one component:
        SEQUENCE b = (SEQUENCE) a.getComponentAt(0);
        // b has 3 components:
        // b's first component is an integer, 2nd and 3rd are sequences
        // let's look at the third one:
        SEQUENCE c = (SEQUENCE) b.getComponentAt(2);
        // c has two components:
        // first is object id, second is CON_SPEC:
        CON_SPEC d = (CON_SPEC) c.getComponentAt(1);
        // d has exactly one component, and it is an octet_string:
        OCTET_STRING e = (OCTET_STRING) d.getComponentAt(0);
        byte[] value = e.getWholeValue();
        InputStream resultStream = new ByteArrayInputStream(value);

        // WILL THE FILES WE RECEIVE ALWAYS HAVE THIS STRUCTURE???

        Part r = (Part) new MimeBodyPart(resultStream);
        String text = (String) r.getContent();
        return text;
    }
}