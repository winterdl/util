!     Module generated by fmodpy for fortran file named 'BOOTSTRAPPED_BOX_SPLINES'     
!=====================================================================
MODULE BOOTSTRAPPED_BOX_SPLINES_WRAPPER
  ! Any necessary "USE" statements
  USE ISO_FORTRAN_ENV
  USE BOOTSTRAPPED_BOX_SPLINES
  ! Make sure it is clear that no implicit types are used in this wrapper
  IMPLICIT NONE
  ! Any interfaces defined for "PROCEDURE" declarations
  
CONTAINS
  !     Fortran wrapper for COMPUTE_BOXES, callable from C     
  !========================================================

  SUBROUTINE c_COMPUTE_BOXES( X_DATA_0, X_DATA_1, X_DATA, RESPONSE, BO&
     &XES_0, BOXES_1, BOXES, WIDTHS, WEIGHTS, BATCH_SIZE, BATCH_SIZE_P&
     &RESENT ) BIND(c)
    ! This subroutine's only purpose is to call the source fortran
    !  code while also being accessible from C.
    INTEGER, INTENT(IN) :: X_DATA_0
    INTEGER, INTENT(IN) :: X_DATA_1
    REAL(KIND=REAL64), DIMENSION(X_DATA_0,X_DATA_1), INTENT(IN) :: X_D&
         &ATA
    REAL(KIND=REAL64), DIMENSION(SIZE(X_DATA,2)), INTENT(IN) :: RESPON&
         &SE
    INTEGER, INTENT(IN) :: BOXES_0
    INTEGER, INTENT(IN) :: BOXES_1
    REAL(KIND=REAL64), DIMENSION(BOXES_0,BOXES_1), INTENT(INOUT) :: BO&
         &XES
    REAL(KIND=REAL64), DIMENSION(SIZE(BOXES,2)), INTENT(OUT) :: WIDTHS
    REAL(KIND=REAL64), DIMENSION(SIZE(BOXES,2)), INTENT(OUT) :: WEIGHT&
         &S
    LOGICAL, INTENT(IN) :: BATCH_SIZE_PRESENT
    INTEGER(KIND=INT64), INTENT(IN), OPTIONAL :: BATCH_SIZE
    ! Preparation code before function call (copying character arrays)
    
    ! Calling source fortran function
    IF (.NOT. BATCH_SIZE_PRESENT) THEN
       CALL COMPUTE_BOXES(X_DATA, RESPONSE, BOXES, WIDTHS, WEIGHTS)
    ELSE
       CALL COMPUTE_BOXES(X_DATA, RESPONSE, BOXES, WIDTHS, WEIGHTS, BA&
            &TCH_SIZE=BATCH_SIZE)
    ENDIF
    ! Copying out any necessary values for return (character arrays)
    
  END SUBROUTINE c_COMPUTE_BOXES


  !     Fortran wrapper for MAX_BOXES, callable from C     
  !========================================================

  SUBROUTINE c_MAX_BOXES( PTS_0, PTS_1, PTS, BOX_CENTERS_0, BOX_CENTER&
     &S, BOX_WIDTHS ) BIND(c)
    ! This subroutine's only purpose is to call the source fortran
    !  code while also being accessible from C.
    INTEGER, INTENT(IN) :: PTS_0
    INTEGER, INTENT(IN) :: PTS_1
    REAL(KIND=REAL64), DIMENSION(PTS_0,PTS_1), INTENT(IN) :: PTS
    INTEGER, INTENT(IN) :: BOX_CENTERS_0
    INTEGER, DIMENSION(BOX_CENTERS_0), INTENT(IN) :: BOX_CENTERS
    REAL(KIND=REAL64), DIMENSION(2*SIZE(BOX_CENTERS,1),SIZE(BOX_CENTER&
         &S,1)), INTENT(OUT) :: BOX_WIDTHS
    ! Preparation code before function call (copying character arrays)
    
    ! Calling source fortran function
    CALL MAX_BOXES(PTS, BOX_CENTERS, BOX_WIDTHS)
    ! Copying out any necessary values for return (character arrays)
    
  END SUBROUTINE c_MAX_BOXES


  !     Fortran wrapper for EVAL_BOX_COEFS, callable from C     
  !========================================================

  SUBROUTINE c_EVAL_BOX_COEFS( BOXES_0, BOXES_1, BOXES, WIDTHS_0, WIDT&
     &HS, X_POINTS_0, X_POINTS_1, X_POINTS, BOX_VALS ) BIND(c)
    ! This subroutine's only purpose is to call the source fortran
    !  code while also being accessible from C.
    INTEGER, INTENT(IN) :: BOXES_0
    INTEGER, INTENT(IN) :: BOXES_1
    REAL(KIND=REAL64), DIMENSION(BOXES_0,BOXES_1), INTENT(IN) :: BOXES
    INTEGER, INTENT(IN) :: WIDTHS_0
    REAL(KIND=REAL64), DIMENSION(WIDTHS_0), INTENT(IN) :: WIDTHS
    INTEGER, INTENT(IN) :: X_POINTS_0
    INTEGER, INTENT(IN) :: X_POINTS_1
    REAL(KIND=REAL64), DIMENSION(X_POINTS_0,X_POINTS_1), INTENT(IN) ::&
         & X_POINTS
    REAL(KIND=REAL64), DIMENSION(SIZE(BOXES,2),SIZE(X_POINTS,2)), INTE&
         &NT(OUT) :: BOX_VALS
    ! Preparation code before function call (copying character arrays)
    
    ! Calling source fortran function
    CALL EVAL_BOX_COEFS(BOXES, WIDTHS, X_POINTS, BOX_VALS)
    ! Copying out any necessary values for return (character arrays)
    
  END SUBROUTINE c_EVAL_BOX_COEFS


  !     Fortran wrapper for EVAL_BOXES, callable from C     
  !========================================================

  SUBROUTINE c_EVAL_BOXES( BOXES_0, BOXES_1, BOXES, WIDTHS_0, WIDTHS, &
     &WEIGHTS_0, WEIGHTS, X_POINTS_0, X_POINTS_1, X_POINTS, RESPONSE )&
     & BIND(c)
    ! This subroutine's only purpose is to call the source fortran
    !  code while also being accessible from C.
    INTEGER, INTENT(IN) :: BOXES_0
    INTEGER, INTENT(IN) :: BOXES_1
    REAL(KIND=REAL64), DIMENSION(BOXES_0,BOXES_1), INTENT(IN) :: BOXES
    INTEGER, INTENT(IN) :: WIDTHS_0
    REAL(KIND=REAL64), DIMENSION(WIDTHS_0), INTENT(IN) :: WIDTHS
    INTEGER, INTENT(IN) :: WEIGHTS_0
    REAL(KIND=REAL64), DIMENSION(WEIGHTS_0), INTENT(IN) :: WEIGHTS
    INTEGER, INTENT(IN) :: X_POINTS_0
    INTEGER, INTENT(IN) :: X_POINTS_1
    REAL(KIND=REAL64), DIMENSION(X_POINTS_0,X_POINTS_1), INTENT(IN) ::&
         & X_POINTS
    REAL(KIND=REAL64), DIMENSION(SIZE(X_POINTS,2)), INTENT(OUT) :: RES&
         &PONSE
    ! Preparation code before function call (copying character arrays)
    
    ! Calling source fortran function
    CALL EVAL_BOXES(BOXES, WIDTHS, WEIGHTS, X_POINTS, RESPONSE)
    ! Copying out any necessary values for return (character arrays)
    
  END SUBROUTINE c_EVAL_BOXES


  !     Fortran wrapper for QSORTC, callable from C     
  !========================================================

  SUBROUTINE c_QSORTC( A_0, A, IDX ) BIND(c)
    ! This subroutine's only purpose is to call the source fortran
    !  code while also being accessible from C.
    INTEGER, INTENT(IN) :: A_0
    REAL(KIND=REAL64), DIMENSION(A_0), INTENT(INOUT) :: A
    INTEGER, DIMENSION(SIZE(A)), INTENT(OUT) :: IDX
    ! Preparation code before function call (copying character arrays)
    
    ! Calling source fortran function
    CALL QSORTC(A, IDX)
    ! Copying out any necessary values for return (character arrays)
    
  END SUBROUTINE c_QSORTC

END MODULE BOOTSTRAPPED_BOX_SPLINES_WRAPPER
