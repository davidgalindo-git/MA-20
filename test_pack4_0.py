''' Testeur de fonction pack4
JCY pour les étudiants (version sans la fonction pack4, à remplacer)
05.02.25
'''

#coller ici votre fonction pack4, pour l'instant ne fait rien, mais renvoie sans rien bouger
def pack4(a,b,c,d):
    nm=0
    if c==0 and d!=0:
        a,b,c,d=a,b,d,0
        nm+=1
    if b==0 and c!=0:
        a,b,c,d=a,c,d,0
        nm+=1
    if a==0 and b!=0:
        a,b,c,d=b,c,d,0
        nm+=1
    if a==b and a>0:
        a = 2*a
        b=c
        c=d
        d=0
        nm+=1
    if b==c and b>0:
        b=2*b
        c=d
        d=0
        nm+=1
    if c==d and c>0:
        c=2*c
        d=0
        nm+=1
    return[a,b,c,d,nm]


# tableau des valeurs de test
tests_inputs=[[0,0,0,0],[0,0,0,2],[0,0,2,2],[0,2,2,2],[2,2,2,2],[2,0,2,2],
            [0,2,2,4],[2,0,2,4],[0,4,2,2],[2,2,4,4],[2,4,4,8],[0,2,4,8]]

# tableau des solutions attendues
expected_outputs=[[0,0,0,0,0],[2,0,0,0,3],[4,0,0,0,3],[4,2,0,0,2],[4,4,0,0,2],[4,2,0,0,2],
            [4,4,0,0,2],[4,4,0,0,2],[4,4,0,0,2],[4,8,0,0,2],[2,8,8,0,1],[2,4,8,0,1]]

def test_pack4():
    for itest in range(len(tests_inputs)):
        test_input=tests_inputs[itest]
        expected_output=expected_outputs[itest]

        # envoi de la fonction et récupération des résultats (adapter suivant le retour)
        [a1,b1,c1,d1,e1] = pack4(test_input[0],test_input[1],test_input[2],test_input[3])

        # Vérification du contenu
        if (a1,b1,c1,d1,e1) == (expected_output[0],expected_output[1],expected_output[2],expected_output[3], expected_output[4]):
            print ("Réussi: valeur testée: ",test_input,"  attendu: ", expected_output)
        else:
            if (a1,b1,c1,d1) != (expected_output[0],expected_output[1],expected_output[2],expected_output[3]):
                print ("ERREUR    pb fusion: ",test_input,"  attendu: ", expected_output, " retourné: ", [a1,b1,c1,d1,e1] )
            if e1 != expected_output[4] :
                print ("WARNING pb comptage:", test_input,"  attendu: ", expected_output, " retourné: ", [a1,b1,c1,d1,e1] )

test_pack4()
         