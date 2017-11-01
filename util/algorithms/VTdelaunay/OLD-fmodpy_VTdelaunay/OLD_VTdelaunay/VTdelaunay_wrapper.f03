MODULE VTDELAUNAY_WRAPPER
  USE ISO_C_BINDING, ONLY: C_LONG, C_DOUBLE, C_INT
  USE REAL_PRECISION
  USE VTDELAUNAY
  IMPLICIT NONE

CONTAINS


SUBROUTINE c_DELAUNAYP( D, N, PTS, P, EPS, SIMP, WEIGHTS, ERR ) BIND(c&
     &)
    INTEGER(KIND=C_LONG), INTENT(IN) :: D
    INTEGER :: TEMP_D
    INTEGER(KIND=C_LONG), INTENT(IN) :: N
    INTEGER :: TEMP_N
    REAL(KIND=C_DOUBLE), INTENT(IN), DIMENSION(D,N) :: PTS
    REAL(KIND=C_DOUBLE), INTENT(IN), DIMENSION(D) :: P
    REAL(KIND=C_DOUBLE), INTENT(IN) :: EPS
    INTEGER(KIND=C_LONG), INTENT(OUT), DIMENSION(D+1) :: SIMP
    INTEGER, DIMENSION(D+1) :: TEMP_SIMP
    REAL(KIND=C_DOUBLE), INTENT(OUT), DIMENSION(D+1) :: WEIGHTS
    INTEGER(KIND=C_LONG), INTENT(OUT) :: ERR
    INTEGER :: TEMP_ERR
    ! WARNING: Automatically generated the following copies to handle a
    ! type-mismatch. NumPy uses 64-bit (KIND=REAL64) INTEGERs and REALs.
    ! Consider converting 'DELAUNAYP' to (KIND=REAL64) for better performance.
    TEMP_D = D
    TEMP_N = N
    TEMP_SIMP = SIMP
    TEMP_ERR = ERR
    CALL DELAUNAYP(TEMP_D, TEMP_N, PTS, P, EPS, TEMP_SIMP, WEIGHTS, TE&
         &MP_ERR)
    SIMP = TEMP_SIMP
    ERR = TEMP_ERR
  END SUBROUTINE c_DELAUNAYP
END MODULE VTDELAUNAY_WRAPPER