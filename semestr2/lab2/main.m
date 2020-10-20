function main()
    beginp = -5
    endp = 5
    deltap = 0.1
    x = beginp:deltap:endp;
    mu = 0;
    sigma = 1;
    a = -1;
    b = 1;
    
   % Change default axes fonts.
    set(0,'DefaultAxesFontName', 'Times New Roman')
    set(0,'DefaultAxesFontSize', 14);

    % Change default text fonts.
    set(0,'DefaultTextFontname', 'Times New Roman');
    set(0,'DefaultTextFontSize', 14);
    
    f1 = normcdf(x,mu,sigma);
    subplot(2,2,1)
    plot(x, f1, 'LineWidth', 2);
    title({'График функции', 'нормального распределения'});  
    text((beginp + endp) / 2 + 1, deltap, ['$\mu = $' num2str(mu)],'interpreter','latex');
    text((beginp + endp) / 2 + 1, 2 * deltap, ['$\sigma = $' num2str(sigma)],'interpreter','latex');
    
    grid on;
   
    f2 = unifcdf(x, a, b);
    subplot(2,2,2)
    plot(x, f2, 'LineWidth', 2, 'Color', 'm');
    title({'График функции', 'равномерного распределения'});
    text((beginp + endp) / 2 + 1, deltap, ['a = ' num2str(a)],'interpreter','latex');
    text((beginp + endp) / 2 + 1, 2 * deltap, ['b = ' num2str(b)],'interpreter','latex');

    grid on;
    
    p1 = normpdf(x,mu,sigma);
    subplot(2,2,3)
    plot(x, p1, 'LineWidth', 2, 'Color', 'red');
    title({'График функции плотности', 'нормального распределения'});
    text(endp - 2, deltap, ['$\mu = $' num2str(mu)],'interpreter','latex');
    text(endp - 2, 2 * deltap, ['$\sigma = $' num2str(sigma)],'interpreter','latex');
    
    grid on;
    
    p2 = unifpdf(x, a, b);
    subplot(2,2,4)
    plot(x, p2, 'LineWidth', 2, 'Color', [.1 .7 .7]);
    title({'График функции плотности', 'равномерного распределения'});
    text(endp - 2, deltap, ['a = ' num2str(a)],'interpreter','latex');
    text(endp - 2, 2 * deltap, ['b = ' num2str(b)],'interpreter','latex');
end